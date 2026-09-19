import hashlib
import json
import requests
from datetime import datetime
import concurrent.futures
import sys

print("=== ASHTE MOBILE: API TOKEN SCRAPER ===")

json_file = "ashtemobile94.json"

# تووکنەکەی خۆت کە لە وێنەکەدا هەیە
API_TOKEN = "33833|hNBTRwESKR8UJGSdTO6O1PzF35LT0WJNyHKsA5925266286a"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.6.1 Mobile/15E148 Safari/604.1"
}

session = requests.Session()
session.headers.update(headers)

raw_apps = []

print("Step 1: Fetching games using API Token...")
try:
    res = session.get("https://check0ver.net/api/iapps?page=1", timeout=15)
    if res.status_code != 200:
        print(f"CRITICAL ERROR: Status Code {res.status_code}")
        sys.exit(1)
        
    data = res.json()
    # ئەگەر داتاکە ڕاستەوخۆ لیست بوو یان لەناو paginator بوو
    items = data.get("data", []) or data.get("props", {}).get("paginator", {}).get("data", [])
    if not items:
        # ئەگەر داتاکە خۆی لیست بوو
        if isinstance(data, list):
            items = data
        else:
            sys.exit(1)
            
    raw_apps.extend(items)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

for page in range(2, 165):
    try:
        r = session.get(f"https://check0ver.net/api/iapps?page={page}", timeout=10)
        if r.status_code != 200:
            break
        data = r.json()
        items = data.get("data", []) or data.get("props", {}).get("paginator", {}).get("data", [])
        if not items:
            break
        raw_apps.extend(items)
    except:
        break

print(f"Step 2: Extracting links for {len(raw_apps)} apps...")

def get_real_app(item):
    name = item.get("name", "Unknown App")
    version = item.get("version", "1.0")
    icon_url = item.get("image", "https://ashtemobile.site/logo.png")
    uuid = item.get("uuid", "")
    
    bundle = item.get("bundle")
    if not bundle or " " in bundle:
        bundle = f"com.ashtemobile.{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
    # هێنانی لینکی داونلۆد بە ڕێگەی API
    req_url = f"https://check0ver.net/api/iapps/{uuid}/download"
    real_link = None
    
    try:
        dl_res = session.get(req_url, allow_redirects=False, timeout=10)
        if dl_res.status_code in [301, 302, 303, 307, 308]:
            link = dl_res.headers.get('Location', '')
            if "ref=" in link or "check0ver" in link:
                real_link = link
        elif dl_res.status_code == 200:
            link = dl_res.json().get('url', '')
            if "ref=" in link or "check0ver" in link:
                real_link = link
    except:
        pass
        
    if not real_link:
        return None
        
    if ".ipa" not in real_link.split("?")[0]:
        connector = "&" if "?" in real_link else "?"
        real_link += f"{connector}file={hashlib.md5(uuid.encode()).hexdigest()}.ipa"
        
    return {
        "name": name,
        "bundleIdentifier": bundle,
        "developerName": "AshteMobile / Check0ver",
        "version": version,
        "versionDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "versionDescription": "Direct CDN Link",
        "downloadURL": real_link,
        "localizedDescription": f"Original CDN Link for {name}",
        "iconURL": icon_url,
        "tintColor": "#04ecfc",
        "size": 314572800,
        "versions": [
            {
                "version": version,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "localizedDescription": "Direct Release",
                "downloadURL": real_link,
                "size": 314572800,
                "minOSVersion": "14.0"
            }
        ]
    }

apps_list = []
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    results = executor.map(get_real_app, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

source_structure = {
    "name": "Ashtemobile",
    "identifier": "com.ashtemobile.source", 
    "subtitle": "Ksign & Feather Source",
    "description": "100% Real Direct CDN Links via API Token.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "tintColor": "#ff007f",
    "apps": apps_list,
    "news": []
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"Done! Saved {len(apps_list)} games to {json_file}")
