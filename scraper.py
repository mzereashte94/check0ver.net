import os
import json
import requests
import subprocess
import concurrent.futures

GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY")
RELEASE_TAG = "tryipa-files"

# دروستکردنی بەشی Releases بۆ فایلی نوێ
subprocess.run(
    ["gh", "release", "create", RELEASE_TAG, "--title", "TryIPA Files", "--notes", "Automated IPA uploads from TryIPA"], 
    env=os.environ, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

existing_files = []
try:
    out = subprocess.check_output(["gh", "release", "view", RELEASE_TAG, "--json", "assets"], env=os.environ)
    existing_files = [asset["name"] for asset in json.loads(out).get("assets", [])]
except:
    pass

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55"
}

print("Fetching apps list from tryipa.com...")

# هێنانی داتای سایتەکە لە ڕێگەی API
api_url = "https://tryipa.com/api/apps" 
try:
    response = requests.get(api_url, headers=headers, timeout=15)
    response.raise_for_status()
    all_apps = response.json()
except Exception as e:
    print(f"Failed to fetch apps list: {e}")
    all_apps = []

print(f"Found {len(all_apps)} apps.")

# بۆ تاقیکردنەوە، تەنها یەکەم 5 بەرنامە وەردەگرین بۆ ئەوەی کات زۆر نەبات
apps_to_process = all_apps[:5]

def process_app(app):
    name = app.get("name", "Unknown")
    version = app.get("version", "1.0")
    download_url = app.get("download_url")
    
    if not download_url:
        print(f"No download URL for {name}")
        return None

    safe_name = "".join(x for x in name if x.isalnum() or x in " -_").replace(" ", "_")
    local_filename = f"{safe_name}_{version}.ipa"

    if local_filename in existing_files:
        print(f"Already exists: {name}")
        return app

    print(f"-> Processing: {name}")
    try:
        # هەوڵی داونلۆدکردن
        with requests.get(download_url, headers=headers, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        downloaded_size = os.path.getsize(local_filename)
        
        # پشکنین بزانین سایزەکەی زۆر بچووک نییە (کە نیشانەی بلۆکبوونە)
        if downloaded_size < 1 * 1024 * 1024:
            print(f"--- FAKE/BLOCKED FILE DETECTED for {name} ({downloaded_size} bytes).")
            os.remove(local_filename)
            return None
            
        print(f"+++ Uploading {name} ({downloaded_size} bytes)...")
        upload = subprocess.run(["gh", "release", "upload", RELEASE_TAG, local_filename, "--clobber"], env=os.environ, capture_output=True)
        
        if upload.returncode == 0:
            print(f"+++ SUCCESS: {name} uploaded.")
        else:
            print(f"--- FAILED to upload {name}: {upload.stderr}")
            
        if os.path.exists(local_filename):
            os.remove(local_filename)
            
        return app
            
    except Exception as e:
        print(f"--- Error with {name}: {e}")
        if os.path.exists(local_filename):
            os.remove(local_filename)
        return None

# کارپێکردن بە خێرایی
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    list(executor.map(process_app, apps_to_process))

print("Quick test finished.")
