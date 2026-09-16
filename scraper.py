import os
import json
import requests
import subprocess
import concurrent.futures

GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY")
RELEASE_TAG = "ipa-files"

# 1. دروستکردنی بەشی Releases ئەگەر نەبوو
subprocess.run(
    ["gh", "release", "create", RELEASE_TAG, "--title", "IPA Files", "--notes", "Automated IPA uploads"], 
    env=os.environ, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

# 2. هێنانی لیستی ئەو فایلانەی پێشتر ئەپلۆد کراون بۆ ئەوەی دووبارە نەکرێنەوە
existing_files = []
try:
    out = subprocess.check_output(["gh", "release", "view", RELEASE_TAG, "--json", "assets"], env=os.environ)
    existing_files = [asset["name"] for asset in json.loads(out).get("assets", [])]
except:
    pass

# 3. خوێندنەوەی فایلی JSON ەکەی خۆت
json_file = "ashtemobile94.json"
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

apps = data.get("apps", [])
print(f"Found {len(apps)} apps in {json_file}")

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55"
}

def process_app(app):
    name = app.get("name", "Unknown")
    version = app.get("version", "1.0")
    
    # پشکنینی قەبارە (ئەگەر لە ١ گێگا زیاتر بوو، وازی لێ دەهێنێت)
    size = app.get("size", 0)
    size_bytes = 0
    if isinstance(size, int) or isinstance(size, float):
        size_bytes = int(size)
    elif isinstance(size, str):
        try:
            if "GB" in size.upper():
                size_bytes = int(float(size.upper().replace("GB", "").strip()) * 1024 * 1024 * 1024)
            elif "MB" in size.upper():
                size_bytes = int(float(size.upper().replace("MB", "").strip()) * 1024 * 1024)
        except:
            pass
            
    if size_bytes >= (1 * 1024 * 1024 * 1024):
        print(f"Skipping {name}: Size is over 1GB")
        return app

    # وەرگرتنی لینکەکە لەناو فایلەکەی خۆت
    original_url = app.get("downloadURL") or app.get("install_url")

    # ئەگەر پێشتر لینکەکەی کرابوو بە گیت هاب یان بەتاڵ بوو، وازی لێ بهێنە
    if not original_url or "github.com" in original_url:
        return app

    safe_name = "".join(x for x in name if x.isalnum() or x in " -_").replace(" ", "_")
    local_filename = f"{safe_name}_{version}.ipa"
    github_direct_url = f"https://github.com/{GITHUB_REPO}/releases/download/{RELEASE_TAG}/{local_filename}"

    # ئەگەر پێشتر ئەپلۆد کراوە بەس لینکەکەی دەگۆڕێت
    if local_filename in existing_files:
        app["downloadURL"] = github_direct_url
        app["install_url"] = github_direct_url
        if "versions" in app and len(app["versions"]) > 0:
            app["versions"][0]["downloadURL"] = github_direct_url
        return app

    print(f"Downloading: {name} ...")
    try:
        # چارەسەرکردنی ڕیدایریکت (بۆ دۆزینەوەی فایلی ipa ی ڕاستەقینە)
        final_link = original_url
        res = requests.get(original_url, headers=headers, allow_redirects=False, timeout=10)
        if res.status_code in [301, 302, 303, 307, 308] and "Location" in res.headers:
            final_link = res.headers["Location"]
            
        # داونلۆدکردن
        with requests.get(final_link, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"Uploading {name} to GitHub Releases...")
        upload = subprocess.run(["gh", "release", "upload", RELEASE_TAG, local_filename, "--clobber"], env=os.environ, capture_output=True)
        
        if upload.returncode == 0:
            # لێرەدا لینکە کۆنەکە دەسڕێتەوە و هی گیت هاب دادەنێت!
            app["downloadURL"] = github_direct_url
            app["install_url"] = github_direct_url
            if "versions" in app and len(app["versions"]) > 0:
                app["versions"][0]["downloadURL"] = github_direct_url
            print(f"SUCCESS: {name}")
        else:
            print(f"FAILED to upload {name}")
            
        if os.path.exists(local_filename):
            os.remove(local_filename)
            
    except Exception as e:
        print(f"Error with {name}: {e}")
        if os.path.exists(local_filename):
            os.remove(local_filename)

    return app

# کارپێکردنی ٣ داونلۆد لە یەک کاتدا بۆ خێرایی
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    updated_apps = list(executor.map(process_app, apps))

data["apps"] = updated_apps

# خەزنکردنەوەی فایلی JSON ەکە بە لینکە نوێکانەوە
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Done! JSON file updated successfully.")
