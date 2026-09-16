import hashlib
import json
import re
import requests
import concurrent.futures

base_url = "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf&page="

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "X-Requested-With": "XMLHttpRequest"
}

print("1. Fetching app list automatically...")
raw_apps = []

for page in range(1, 10):  # دەتوانیت ژمارەی پەڕەکان زیاد بکەیت
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

print(f"Found {len(raw_apps)} apps. Extracting direct .ipa?ref= links automatically...")

def get_automated_ipa_link(app):
    uuid = app.get("uuid")
    name = app.get("name")
    version = app.get("version", "1.0")
    size_str = app.get("size", "0 MB")
    image_url = app.get("image", "https://ashtemobile.site/logo.png")
    updated_at = app.get("updatedAt", "2026-09-15T00:00:00+00:00")
    bundle = app.get("bundle", f"com.ashtemobile.{uuid}")
    
    detail_page_url = f"https://check0ver.net/en/iapps/{uuid}"
    resolved_download_url = detail_page_url

    try:
        # چوونە ناو پەڕەی یارییەکە بۆ دۆزینەوەی خۆکاری لینکی داونلۆود
        res = requests.get(detail_page_url, headers=headers, timeout=10)
        if res.status_code == 200:
            # گەڕان بەدوای پاتەرنی لینکی .ipa?ref= لەناو سورسکرێپتی پەڕەکەدا
            match_ref = re.search(r'https?://[^\s<>"]+?/api/check0ver/[^\s<>"]+?\.ipa\?ref=[^\s<>"]+', res.text)
            if match_ref:
                resolved_download_url = match_ref.group(0)
            else:
                # ئەگەر لە شێوازی تردا بوو، گەڕان بەدوای هەر لینکێکی .ipa کە refـی هەبێت
                match_general = re.search(r'https?://[^\s<>"]+?\.ipa\?[^\s<>"]+', res.text)
                if match_general:
                    resolved_download_url = match_general.group(0)
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
        "install_url": resolved_download_url,
        "download_url": resolved_download_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "Auto Extracted Source",
        "localizedDescription": "Automatically extracted IPA link.",
        "iconURL": image_url if image_url else "https://ashtemobile.site/logo.png",
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": updated_at,
                "localizedDescription": None,
                "downloadURL": resolved_download_url,
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
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(get_automated_ipa_link, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "Auto-Extracted Direct IPA Source",
    "description": "Source with automatically extracted download links.",
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

print(f"Done! Automatically extracted links for {len(apps_list)} apps.")
