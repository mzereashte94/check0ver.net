import os
import json
import subprocess
import concurrent.futures
import cloudscraper

GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY")
RELEASE_TAG = "ipa-files"

# دروستکردنی بەشی Releases
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

# بەکارهێنانی Cloudscraper بۆ خۆدزینەوە لە بلۆکی سایتەکە
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'ios', 'mobile': True})

def process_app(app):
    name = app.get("name", "Unknown")
    version = app.get("version", "1.0")
    
    size_str = str(app.get("size", "0")).upper()
    if "GB" in size_str:
        return app  # فەرامۆشکردنی فایلی سەروو ١ گێگا

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

    print(f"-> Processing: {name}")
    try:
        final_link = None
        
        # هێنانی لینکی ڕاستەقینە بە بەکارهێنانی scraper
        res = scraper.get(original_url, allow_redirects=False, timeout=15)
        if res.status_code in [301, 302, 303, 307, 308] and "Location" in res.headers:
            final_link = res.headers["Location"]
            
        if not final_link and "/en/iapps/" in original_url:
            api_url = original_url.replace("/en/iapps/", "/api/iapps/")
            res_api = scraper.get(api_url, allow_redirects=False, timeout=15)
            if res_api.status_code in [301, 302, 303, 307, 308] and "Location" in res_api.headers:
                final_link = res_api.headers["Location"]

        if not final_link:
            print(f"--- FAILED to bypass Cloudflare for {name}")
            return app

        # داونلۆدکردنی فایلەکە
        with scraper.get(final_link, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # پشکنینی قەبارە: ئەگەر لە ٥ مێگابایت بچووکتر بوو، واتە ساختەیە و دەیسڕێتەوە
        downloaded_size = os.path.getsize(local_filename)
        if downloaded_size < 5 * 1024 * 1024:
            print(f"--- FAKE/BLOCKED FILE DETECTED ({downloaded_size} bytes). Deleted.")
            os.remove(local_filename)
            return app
        
        print(f"+++ Uploading {name} ({downloaded_size} bytes)...")
        upload = subprocess.run(["gh", "release", "upload", RELEASE_TAG, local_filename, "--clobber"], env=os.environ, capture_output=True)
        
        if upload.returncode == 0:
            app["downloadURL"] = github_direct_url
            app["install_url"] = github_direct_url
            if "versions" in app and len(app["versions"]) > 0:
                app["versions"][0]["downloadURL"] = github_direct_url
            print(f"+++ SUCCESS: {name}")
            
        if os.path.exists(local_filename):
            os.remove(local_filename)
            
    except Exception as e:
        print(f"--- Error with {name}")
        if os.path.exists(local_filename):
            os.remove(local_filename)

    return app

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    updated_apps = list(executor.map(process_app, apps))

data["apps"] = updated_apps
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Done! JSON file updated successfully.")
