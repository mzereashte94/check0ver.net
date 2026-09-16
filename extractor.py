import hashlib
import json
import re
import requests
import concurrent.futures

base_url = "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf&page="

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "X-Requested-With": "XMLHttpRequest"
}

print("1. Fetching apps to extract direct IPA links...")
raw_apps = []

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
        else:
            break
    except:
        pass

print(f"Found {len(raw_apps)} apps. Extracting direct .ipa?ref= links...")

def get_direct_ipa(app):
    uuid = app.get("uuid")
    name = app.get("name")
    version = app.get("version", "1.0")
    size_str = app.get("size", "0 MB")
    image_url = app.get("image", "https://ashtemobile.site/logo.png")
    updated_at = app.get("updatedAt", "2026-09-15T00:00:00+00:00")
    bundle = app.get("bundle", f"com.ashtemobile.{uuid}")
    
    # لینکی فەرمی API بۆ وەرگرتنی لینکە ڕاستەوخۆکە
    api_download_url = f"https://check0ver.net/api/iapps/{uuid}/download"
    fallback_url = f"https://check0ver.net/en/iapps/{uuid}"
    resolved_ipa_url = fallback_url

    try:
        # هەوڵدان بۆ گرتنی لینکی ڕاستەوخۆ لە ڕێگەی APIـیەوە
        res = requests.get(api_download_url, headers=headers, allow_redirects=True, timeout=5)
        
        # پشکنینی ئایا لینکێکی .ipa لە وەڵامەکەدا هەیە یان نا
        if ".ipa" in res.text:
            # گەڕان بەدوای لینکێکی پڕ لە ref یان .ipa لە ناو وەڵامەکەدا
            url_match = re.search(r'https?://[^\s<>"]+?\.ipa[^\s<>"]*', res.text)
            if url_match:
                resolved_ipa_url = url_match.group(0)
        elif res.status_code in [301, 302, 303, 307, 308]:
            loc = res.headers.get("Location", "")
            if ".ipa" in loc:
                resolved_ipa_url = loc
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
        "install_url": resolved_ipa_url,
        "download_url": resolved_ipa_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "Direct IPA Source",
        "localizedDescription": "Extracted with direct .ipa link.",
        "iconURL": image_url if image_url else "https://ashtemobile.site/logo.png",
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": updated_at,
                "localizedDescription": None,
                "downloadURL": resolved_ipa_url,
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
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    results = executor.map(get_direct_ipa, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "Direct IPA Source",
    "description": "Source with extracted direct IPA links.",
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

print(f"Done! Processed {len(apps_list)} apps with direct link extraction.")
