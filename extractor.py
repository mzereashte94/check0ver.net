import hashlib
import json
import re
import requests
import concurrent.futures

base_url = "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf&page="
api_dl_base = "https://check0ver.net/api/iapps/{}/download"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
        "AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 "
        "Safari/604.1"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://check0ver.net/"
}

print("1. Fetching all apps from pages...")
raw_apps = []

for page in range(1, 161):
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
        else:
            break
    except Exception as e:
        print(f"Error on page {page}: {e}")

print(f"Found {len(raw_apps)} apps. Extracting REAL .ipa URLs...")

def process_app(app):
    name = app.get("name")
    version = app.get("version", "1.0")
    size_str = app.get("size", "0 MB")
    uuid = app.get("uuid")
    bundle = app.get("bundle", f"com.ashtemobile.{uuid}")
    image_url = app.get("image")
    updated_at = app.get("updatedAt", "2026-09-15T00:00:00+00:00")
    
    # لینکی پێشوەختە (ئەگەر شکستی هێنا ئەمە دادەنێت)
    real_ipa_url = f"https://check0ver.net/en/iapps/{uuid}/download"
    dl_api = api_dl_base.format(uuid)
    
    try:
        r = requests.get(dl_api, headers=headers, allow_redirects=False, timeout=5)
        # ئەگەر سێرڤەر ڕاستەوخۆ ڕیدایریکتی کرد بۆ فایلەکە
        if r.status_code in [301, 302, 303, 307, 308]:
            real_ipa_url = r.headers.get('Location', real_ipa_url)
        # ئەگەر سێرڤەر داتای بە شێوەی جیسۆن داوەتەوە
        elif r.status_code == 200:
            try:
                js_data = r.json()
                for key in ['url', 'download_url', 'downloadURL', 'link', 'file']:
                    if key in js_data and 'ref=' in str(js_data[key]):
                        real_ipa_url = js_data[key]
                        break
            except:
                pass
    except:
        pass

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
        "install_url": real_ipa_url,
        "download_url": real_ipa_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "Awesome App",
        "localizedDescription": "Downloaded from AshteMobile Source.",
        "iconURL": image_url if image_url else "https://ashtemobile.site/logo.png",
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": updated_at,
                "localizedDescription": None,
                "downloadURL": real_ipa_url,
                "size": size_bytes,
                "buildVersion": None,
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
# لێرەدا ژمارەی داواکارییەکانمان کەمکردەوە بۆ 10 بۆ ئەوەی سێرڤەرەکە گیتهاب بلۆک نەکات
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(process_app, raw_apps)
    for result in results:
        if result:
            apps_list.append(result)

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
            "date": "2026-09-15T00:00:00+00:00",
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

print(f"Successfully generated '{output_filename}' with REAL IPA links for {len(apps_list)} apps!")
