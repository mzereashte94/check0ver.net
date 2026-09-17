import hashlib
import json
import re
import requests
import concurrent.futures
from datetime import datetime

print("=== ASHTE MOBILE: RELIABLE GITHUB LINKS EXTRACTOR ===")

base_url = "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf&page="

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

print("1. Fetching apps from source...")
raw_apps = []

# هێنانی داتای پەڕەکان
for page in range(1, 10):
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
                paginator = page_data.get("props", {}).get("paginator", {}).get("data", [])
                
                if not paginator:
                    break
                
                raw_apps.extend(paginator)
    except Exception as e:
        print(f"Error on page {page}: {e}")

print(f"Found {len(raw_apps)} apps! Filtering for PERMANENT GitHub links only...")

def get_real_ipa(app):
    uuid = app.get("uuid")
    name = app.get("name")
    version = app.get("version", "1.0")
    size_str = app.get("size", "0 MB")
    image_url = app.get("image", "https://ashtemobile.site/logo.png")
    updated_at = app.get("updatedAt", datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"))
    bundle = app.get("bundle", f"com.ashtemobile.{uuid}")
    
    download_trigger_url = f"https://check0ver.net/en/iapps/{uuid}/download"
    final_ipa_url = ""
    
    try:
        res = requests.get(download_trigger_url, headers=headers, allow_redirects=False, timeout=5)
        if res.status_code in [301, 302, 303, 307, 308]:
            location = res.headers.get("Location", "")
            if ".ipa" in location:
                final_ipa_url = location
        elif res.status_code == 200:
            api_trigger = f"https://check0ver.net/api/iapps/{uuid}/download"
            res_api = requests.get(api_trigger, headers=headers, allow_redirects=False, timeout=5)
            if res_api.status_code in [301, 302, 303, 307, 308]:
                location = res_api.headers.get("Location", "")
                if ".ipa" in location:
                    final_ipa_url = location
    except:
        pass

    # *** بەشی گرنگ: تەنها ئەو لینکانە قبوڵ دەکات کە هی گیت هابن و هەمیشەیین ***
    if not final_ipa_url or "github.com" not in final_ipa_url.lower():
        return None

    numeric_id = int(hashlib.md5(uuid.encode()).hexdigest()[:8], 16) % (10**9)

    size_bytes = 50 * 1024 * 1024
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
        "icon": image_url if image_url else "https://ashtemobile.site/logo.png",
        "badge": "",
        "type": "games",
        "install_url": final_ipa_url,
        "download_url": final_ipa_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "Safe & Permanent",
        "localizedDescription": "Downloaded from reliable GitHub sources.",
        "iconURL": image_url if image_url else "https://ashtemobile.site/logo.png",
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": updated_at,
                "localizedDescription": None,
                "downloadURL": final_ipa_url, 
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

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(get_real_ipa, raw_apps)
    for res in results:
        # تەنها ئەوانە زیاد دەکات کە لینکی گیت هابیان هەبووە و فلتەرەکەیان بڕیوە
        if res is not None:
            apps_list.append(res)
            print(f"+ Added Safe App: {res['name']}")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all of my apps.",
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
            "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
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

print(f"\nDone! Extracted {len(apps_list)} PERMANENT .ipa URLs.")
print("=== FINISHED ===")
