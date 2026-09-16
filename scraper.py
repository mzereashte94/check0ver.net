import os
import json
import requests
import subprocess
import concurrent.futures

GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY")
RELEASE_TAG = "ipa-files"

# دروستکردنی بەشی Releases ئەگەر نەبوو
subprocess.run(
    ["gh", "release", "create", RELEASE_TAG, "--title", "IPA Files", "--notes", "Automated IPA uploads"], 
    env=os.environ, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

existing_files = []
try:
    out = subprocess.check_output(["gh", "release", "view", RELEASE_TAG, "--json", "assets"], env=os.environ)
    existing_files = [asset["name"] for asset in json.loads(out).get("assets", [])]
except:
    pass

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
    
    # وازهێنان لەو فایلانەی قەبارەیان سەروو ١ گێگایە
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
        return app

    original_url = app.get("downloadURL") or app.get("install_url")
    if not original_url or "github.com" in original_url:
        return app

    safe_name = "".join(x for x in name if x.isalnum() or x in " -_").replace(" ", "_")
    local_filename = f"{safe_name}_{version}.ipa"
    github_direct_url = f"https://github.com/{GITHUB_REPO}/releases/download/{RELEASE_TAG}/{local_filename}"

    if local_filename in existing_files:
        app["downloadURL"] = github_direct_url
        app["install_url"] = github_direct_url
        if "versions" in app and len(app["versions"]) > 0:
            app["versions"][0]["downloadURL"] = github_direct_url
        return app

    print(f"-> Processing: {name} ...")
    try:
        final_link = None
        
        # هەوڵدانی یەکەم بۆ هێنانی لینک
        res = requests.get(original_url, headers=headers, allow_redirects=False, timeout=10)
        if res.status_code in [301, 302, 303, 307, 308] and "Location" in res.headers:
            final_link = res.headers["Location"]
        
        # ئەگەر سایتەکە پەڕەی ئاسایی نارد، بەکارهێنانی فێڵی API بۆ دۆزینەوەی لینکە ڕاستەقینەکە
        if not final_link and "/en/iapps/" in original_url:
            api_url = original_url.replace("/en/iapps/", "/api/iapps/")
            res_api = requests.get(api_url, headers=headers, allow_redirects=False, timeout=10)
            if res_api.status_code in [301, 302, 303, 307, 308] and "Location" in res_api.headers:
                final_link = res_api.headers["Location"]

        if not final_link:
            print(f"--- FAILED to find real IPA link for {name}")
            return app

        print(f"-> Downloading {name} from CDN...")
        with requests.get(final_link, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # پشکنینی زۆر گرنگ: ئەگەر قەبارەی فایلەکە لە 2 مێگابایت کەمتر بوو، واتە ساختەیە و دەبێت بسڕدرێتەوە
        downloaded_size = os.path.getsize(local_filename)
        if downloaded_size < 2 * 1024 * 1024:
            print(f"--- FAKE FILE DETECTED for {name} ({downloaded_size} bytes). Skipping upload.")
            os.remove(local_filename)
            return app
        
        print(f"+++ Uploading {name} ({downloaded_size} bytes) to GitHub Releases...")
        upload = subprocess.run(["gh", "release", "upload", RELEASE_TAG, local_filename, "--clobber"], env=os.environ, capture_output=True)
        
        if upload.returncode == 0:
            app["downloadURL"] = github_direct_url
            app["install_url"] = github_direct_url
            if "versions" in app and len(app["versions"]) > 0:
                app["versions"][0]["downloadURL"] = github_direct_url
            print(f"+++ SUCCESS: {name} uploaded correctly.")
        else:
            print(f"--- FAILED to upload {name}: {upload.stderr}")
            
        if os.path.exists(local_filename):
            os.remove(local_filename)
            
    except Exception as e:
        print(f"--- Error with {name}: {e}")
        if os.path.exists(local_filename):
            os.remove(local_filename)

    return app

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    updated_apps = list(executor.map(process_app, apps))

data["apps"] = updated_apps
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Done! JSON file updated successfully.")
