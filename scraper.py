import hashlib
import json
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from datetime import datetime
import re

print("=== ASHTE MOBILE: CHECK0VER DEEP HTML CRAWLER ===")

json_file = "ashtemobile94.json"
base_url = "https://check0ver.net/en/iapps?page="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

app_links = []
seen_uuids = set()

print("Step 1: Scanning Check0ver website to find game pages...")

# دەتوانیت لێرەدا ژمارەی پەڕەکان زیاد بکەیت (بۆ نموونە لە 1 تا 160)
for page in range(1, 10): 
    url = f"{base_url}{page}"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # دۆزینەوەی داتاکانی پەڕەکە ڕێک وەک ئەوەی لە HTMLـەکەدا هەیە
        app_div = soup.find('div', id='app')
        if not app_div or not app_div.has_attr('data-page'):
            continue
            
        data = json.loads(app_div['data-page'])
        items = data.get("props", {}).get("paginator", {}).get("data", [])
        
        found = 0
        for item in items:
            uuid = item.get("uuid")
            if uuid and uuid not in seen_uuids:
                seen_uuids.add(uuid)
                app_links.append(item)
                found += 1
                
        print(f"Scanned page {page}... Found {found} games.")
        if found == 0:
            break
    except Exception as e:
        print(f"Error on page {page}: {e}")

print(f"\nStep 2: Going INSIDE {len(app_links)} game pages to extract ORIGINAL links...")

apps_list = []

def process_check0ver_app(item):
    try:
        name = item.get("name", "Unknown App")
        uuid = item.get("uuid", "")
        version = item.get("version", "1.0")
        size_str = item.get("size", "300 MB")
        icon_url = item.get("image", "https://ashtemobile.site/logo.png")
        bundle = item.get("bundle", "com.ashtemobile.app")
        
        # چوونە ناوەوەی پەڕەی تایبەتی یارییەکە
        app_page_url = f"https://check0ver.net/en/iapps/{uuid}"
        res = requests.get(app_page_url, headers=headers, timeout=15)
        
        download_url = None
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            page_div = soup.find('div', id='app')
            if page_div and page_div.has_attr('data-page'):
                page_data = json.loads(page_div['data-page'])
                # دەرهێنانی لینکی ئەسڵی لە ناوەڕۆکی پەڕەکە خۆی
                app_details = page_data.get("props", {}).get("iapp", {})
                download_url = app_details.get("downloadURL")
        
        # ئەگەر لەوێدا نەبوو، یەکسەر لینکە باوەکەی بۆ دروست دەکات
        clean_name = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
        if not download_url:
            download_url = f"https://check0ver.net/api/iapps/{uuid}/download?file={clean_name}.ipa"
        else:
            if ".ipa" not in download_url:
                download_url = f"{download_url}?file={clean_name}.ipa"

        numeric_id = int(hashlib.md5(uuid.encode()).hexdigest()[:8], 16) % (10**9)
        
        size_bytes = 300 * 1024 * 1024
        try:
            if "GB" in size_str:
                size_bytes = int(float(size_str.replace("GB", "").strip()) * 1024 * 1024 * 1024)
            elif "MB" in size_str:
                size_bytes = int(float(size_str.replace("MB", "").strip()) * 1024 * 1024)
        except:
            pass

        return {
            "id": numeric_id,
            "name": name,
            "version": version,
            "size": size_str,
            "icon": icon_url,
            "badge": "MOD",
            "type": "games",
            "install_url": download_url,
            "download_url": download_url,
            "bundleIdentifier": bundle,
            "marketplaceID": "",
            "developerName": "AshteMobile",
            "subtitle": "Check0ver Original Source",
            "localizedDescription": f"Original link extracted directly from the website for {name}.",
            "iconURL": icon_url,
            "tintColor": "#04ecfc",
            "category": "games",
            "screenshots": [],
            "versions": [
                {
                    "version": version,
                    "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                    "localizedDescription": None,
                    "downloadURL": download_url,
                    "size": size_bytes,
                    "buildVersion": "1.0",
                    "minOSVersion": "14.0",
                }
            ],
            "appPermissions": {
                "entitlements": [],
                "privacy": {}
            },
            "patreon": [],
        }
    except:
        return None

# بەکارهێنانی سیستەمی خێرا (Threads) بۆ چوونە ناو پەڕەکان
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(process_check0ver_app, app_links)
    for res in results:
        if res:
            apps_list.append(res)
            print(f" + Extracted original link for: {res['name']}")

print(f"\nFinished! Extracted {len(apps_list)} games. Saving to JSON...")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Original links extracted directly from the website posts.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "patreonURL": "https://ashtemobile.site/Ashtemobile.json",
    "tintColor": "#ff007f",
    "featuredApps": [],
    "headerURL": "https://ashtemobile.site/logo.png",
    "apps": apps_list,
    "news": []
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"SUCCESS! Check {json_file}")
