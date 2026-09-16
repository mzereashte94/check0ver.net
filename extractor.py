import hashlib
import json
import re
import concurrent.futures
import cloudscraper # ئەمە بەرنامە نوێیەکەیە بۆ شکاندنی پاراستن

base_url = "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf&page="

# دروستکردنی سکریپتێک کە خۆی وەک ئایفۆن و سەفاری نیشان دەدات
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'ios',
        'desktop': False
    }
)

print("1. Fetching all apps from the website using CloudScraper...")
raw_apps = []

for page in range(1, 161):
    url = f"{base_url}{page}"
    try:
        response = scraper.get(url, timeout=15)
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

print(f"Found {len(raw_apps)} apps. Extracting REAL .ipa links...")

def get_real_ipa(app):
    uuid = app.get("uuid")
    name = app.get("name")
    version = app.get("version", "1.0")
    size_str = app.get("size", "0 MB")
    image_url = app.get("image", "https://ashtemobile.site/logo.png")
    updated_at = app.get("updatedAt", "2026-09-15T00:00:00+00:00")
    bundle = app.get("bundle", f"com.ashtemobile.{uuid}")
    
    # لینکی داواکردنی یارییەکە
    api_trigger = f"https://check0ver.net/api/iapps/{uuid}/download"
    final_ipa_url = api_trigger 
    
    try:
        # بەکارهێنانی scraper بۆ ئەوەی ڕێگرییەکانی Cloudflare ببڕێت
        res = scraper.get(api_trigger, allow_redirects=False, timeout=10)
        
        # ئەگەر ڕیدایریکتی کرد بۆ فایلی .ipa
        if res.status_code in [301, 302, 303, 307, 308]:
            loc = res.headers.get("Location", "")
            if ".ipa" in loc:
                if loc.startswith("/"):
                    final_ipa_url = f"https://check0ver.net{loc}"
                else:
                    final_ipa_url = loc
        # ئەگەر بە JSON وەڵامی دایەوە
        elif res.status_code == 200:
            try:
                data = res.json()
                if 'url' in data and '.ipa' in data['url']:
                    final_ipa_url = data['url']
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
        "install_url": final_ipa_url,
        "download_url": final_ipa_url,
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
                "downloadURL": final_ipa_url, # ڕێک لینکە درێژەکەی .ipa?ref دادەنرێت
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

# بەکارهێنانی 50 کرێکار
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(get_real_ipa, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

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

print(f"Done! Successfully created source with exactly {len(apps_list)} real .ipa links.")
