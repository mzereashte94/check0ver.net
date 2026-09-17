import hashlib
import json
import re
import requests
import concurrent.futures

base_url = "https://ipaomtk.com/games?page="

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

print("1. Fetching all games automatically from ipaomtk.com...")
raw_apps = []

# گەڕان بەدوای پەڕەکان بە هەمان سیستەمی data-page
for page in range(1, 51):
    url = f"{base_url}{page}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            match = re.search(r'data-page="([^"]+)"', response.text)
            if match:
                html_escape_decoded = (
                    match.group(1)
                    .replace("&quot;", '"')
                    .replace("&amp;", "&")
                    .replace("&#039;", "'")
                )
                page_data = json.loads(html_escape_decoded)
                props = page_data.get("props", {})
                
                # دۆزینەوەی یارییەکان لەناو گشت مەرجەکانی پراپسدا
                paginator = (
                    props.get("games", {}) or 
                    props.get("apps", {}) or 
                    props.get("paginator", {}).get("data", [])
                )
                
                if isinstance(paginator, dict):
                    paginator = paginator.get("data", [])
                
                if not paginator:
                    break
                
                raw_apps.extend(paginator)
            else:
                break
        else:
            break
    except Exception as e:
        print(f"Error on page {page}: {e}")
        break

print(f"Found {len(raw_apps)} games. Now extracting direct .ipa links and icons...")

def process_game(app):
    name = app.get("name") or app.get("title", "Unknown Game")
    uuid = app.get("uuid") or app.get("id", "")
    slug = app.get("slug") or name.lower().replace(' ', '-').replace(':', '')
    version = app.get("version", "1.0")
    size_str = str(app.get("size", "250 MB"))
    image_url = app.get("image") or app.get("icon") or "https://ashtemobile.site/logo.png"
    
    # دروستکردنی لینکی ڕەسەنی file.ipaomtk.com
    download_url = f"https://file.ipaomtk.com/{slug}/{slug}-IPAOMTK.COM.ipa"
    
    numeric_id = int(hashlib.md5(str(uuid or name).encode()).hexdigest()[:8], 16) % (10**9)
    bundle = app.get("bundle") or f"com.ashtemobile.{slug.replace('-', '')}"

    size_bytes = 500 * 1024 * 1024
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
        "icon": image_url,
        "badge": "MOD",
        "type": "games",
        "install_url": download_url,
        "download_url": download_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "IPAOMTK Official Game",
        "localizedDescription": f"Extracted automatically from ipaomtk.com",
        "iconURL": image_url,
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": "2026-09-17T00:00:00+00:00",
                "localizedDescription": None,
                "downloadURL": download_url,
                "size": size_bytes,
                "buildVersion": "1.0",
                "minOSVersion": "14.0",
            }
        ],
        "appPermissions": {
            "entitlements": [],
            "privacy": {
                "NSUserTrackingUsageDescription": "Your data will be used to deliver personalized ads to you."
            }
        },
        "patreon": [],
    }

apps_list = []

# بەکارهێنانی خێراییە شێتانەکەی ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(process_game, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all of my games from ipaomtk.com.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "patreonURL": "https://ashtemobile.site/Ashtemobile.json",
    "tintColor": "#ff007f",
    "featuredApps": [],
    "headerURL": "https://ashtemobile.site/logo.png",
    "apps": apps_list,
    "news": [
        {
            "title": "Instagram",
            "identifier": "news_instagram",
            "caption": "Ashtemobile",
            "date": "2026-09-17T00:00:00+00:00",
            "tintColor": "#ff007f",
            "imageURL": "https://ashtemobile.site/logo.png",
            "notify": True,
            "url": "https://www.instagram.com/ashtemobile",
            "appID": None,
        }
    ]
}

output_filename = "ashtemobile94.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"Done! Automatically extracted {len(apps_list)} games from ipaomtk.com into {output_filename}.")
