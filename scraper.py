import os
import json
import re
import requests
import subprocess
import hashlib
import concurrent.futures

# وەرگرتنی زانیاری لە GitHub Actions ەوە
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY") # خۆی ناوی ڕیپۆزیتۆرییەکەت دەدۆزێتەوە
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
RELEASE_TAG = "ipa-files" # ناوی ئەو بەشەی فایلەکانی تێدەچێت لە Releases

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

print("1. Creating Release section if not exists...")
# بەکارهێنانی GitHub CLI بۆ دروستکردنی ڕیلیز
subprocess.run(
    ["gh", "release", "create", RELEASE_TAG, "--title", "IPA Files", "--notes", "Automated IPA uploads"], 
    env=os.environ, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

print("2. Fetching existing assets to avoid re-uploading...")
existing_files = []
try:
    out = subprocess.check_output(["gh", "release", "view", RELEASE_TAG, "--json", "assets"], env=os.environ)
    assets_data = json.loads(out)
    existing_files = [asset["name"] for asset in assets_data.get("assets", [])]
except Exception as e:
    print("Could not fetch existing assets (Maybe release is empty).")

print("3. Fetching all apps from the website...")
base_url = "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf&page="
raw_apps = []

for page in range(1, 161):
    url = f"{base_url}{page}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            match = re.search(r'data-page="([^"]+)"', response.text)
            if match:
                html_escape_decoded = match.group(1).replace("&quot;", '"').replace("&amp;", "&").replace("&#039;", "'")
                page_data = json.loads(html_escape_decoded)
                paginator = page_data.get("props", {}).get("paginator", {}).get("data", [])
                
                if not paginator:
                    break
                raw_apps.extend(paginator)
        else:
            break
    except Exception as e:
        pass

print(f"Found {len(raw_apps)} apps. Processing...")

def process_app(app):
    name = app.get("name", "Unknown")
    version = app.get("version", "1.0")
    size_str = app.get("size", "0 MB")
    uuid = app.get("uuid")
    bundle = app.get("bundle", f"com.ashtemobile.{uuid}")
    image_url = app.get("image", "https://ashtemobile.site/logo.png")
    
    # فلتەرکردنی قەبارە (ئەگەر لە ١ گێگابایت گەورەتر بوو، بەجێی دەهێڵێت)
    size_bytes = 50 * 1024 * 1024
    try:
        if "GB" in size_str:
            size_bytes = int(float(size_str.replace("GB", "").strip()) * 1024 * 1024 * 1024)
        elif "MB" in size_str:
            size_bytes = int(float(size_str.replace("MB", "").strip()) * 1024 * 1024)
    except:
        pass

    if size_bytes >= (1 * 1024 * 1024 * 1024):
        return None # ئەمانە دادەنەبەزێنێت

    # دروستکردنی ناوی فایلەکە
    safe_name = "".join(x for x in name if x.isalnum() or x in " -_").replace(" ", "_")
    local_filename = f"{safe_name}_{version}.ipa"
    github_direct_url = f"https://github.com/{GITHUB_REPO}/releases/download/{RELEASE_TAG}/{local_filename}"

    # ئەگەر فایلەکە پێشتر لە بەشی Releases هەبوو، تەنها لینکەکەی تۆمار دەکات و کات بەفیڕۆ نادات
    if local_filename in existing_files:
        final_download_url = github_direct_url
    else:
        # دۆزینەوەی لینکی ڕاستەقینە
        download_trigger_url = f"https://check0ver.net/en/iapps/{uuid}/download"
        final_ipa_url = download_trigger_url
        try:
            res = requests.get(download_trigger_url, headers=headers, allow_redirects=False, timeout=5)
            if res.status_code in [301, 302, 303, 307, 308]:
                location = res.headers.get("Location", "")
                if ".ipa" in location:
                    final_ipa_url = location
        except:
            pass

        final_download_url = final_ipa_url

        # ئەگەر لینکە ڕاستەقینەکە دۆزرایەوە، داونلۆدی دەکات و ئەپلۆدی دەکات
        if ".ipa" in final_ipa_url:
            print(f"Downloading {name} to GitHub Runner...")
            try:
                with requests.get(final_ipa_url, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                # ئەپلۆدکردن بۆ Releases بە بەکارهێنانی GitHub CLI
                print(f"Uploading {name} to Releases...")
                subprocess.run(
                    ["gh", "release", "upload", RELEASE_TAG, local_filename, "--clobber"], 
                    env=os.environ, check=True
                )
                
                final_download_url = github_direct_url # لینکەکە دەگۆڕێت بۆ گیت هاب دوای سەرکەوتن
                os.remove(local_filename) # سڕینەوە بۆ ئەوەی شوێن نەگرێت
            except Exception as e:
                print(f"Error processing {name}: {e}")
                if os.path.exists(local_filename):
                    os.remove(local_filename)

    numeric_id = int(hashlib.md5(uuid.encode()).hexdigest()[:8], 16) % (10**9)

    return {
        "name": name,
        "bundleIdentifier": bundle,
        "version": version,
        "size": size_bytes,
        "iconURL": image_url if image_url else "https://ashtemobile.site/logo.png",
        "downloadURL": final_download_url,
        "localizedDescription": "Hosted on GitHub Releases by Ashtemobile Auto-Bot."
    }

apps_list = []
# دانانی 5 کرێکار لە ناو GitHub Action (ئینتەرنێتی گیت هاب زۆر خێرایە و بەرگە دەگرێت)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_app, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Apps automatically synced and hosted on GitHub Releases.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "apps": apps_list
}

with open("ashtemobile94.json", "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print("Done! JSON file generated successfully.")
