import json
import hashlib
from datetime import datetime
from playwright.sync_api import sync_playwright

print("=== ASHTE MOBILE: DEDICATED IPAOMTK API SCRAPER ===")

json_file = "ashtemobile94.json"
target_site = "https://ipaomtk.com"

raw_extracted_items = []

def handle_response(response):
    try:
        url = response.url
        if "ipaomtk.com" in url and "json" in response.headers.get("content-type", ""):
            data = response.json()
            if isinstance(data, list):
                raw_extracted_items.extend(data)
            elif isinstance(data, dict):
                for key, val in data.items():
                    if isinstance(val, list):
                        raw_extracted_items.extend(val)
                    elif isinstance(val, dict):
                        for sub_k, sub_v in val.items():
                            if isinstance(sub_v, list):
                                raw_extracted_items.extend(sub_v)
    except:
        pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        viewport={"width": 390, "height": 844}
    )
    page = context.new_page()

    page.on("response", handle_response)

    try:
        page.goto(target_site, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)
        
        for _ in range(4):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            page.wait_for_timeout(2000)
    except Exception as e:
        pass

    browser.close()

apps_list = []
seen_names = set()

for item in raw_extracted_items:
    if not isinstance(item, dict):
        continue
        
    name = item.get("name") or item.get("title") or item.get("appName")
    if not name or name in seen_names:
        continue
    
    download_url = item.get("downloadURL") or item.get("download_url") or item.get("fileUrl") or item.get("url") or ""
    
    if not download_url:
        app_id = item.get("uuid") or item.get("id") or item.get("slug")
        if app_id:
            download_url = f"https://file.ipaomtk.com/{app_id}/{app_id}-IPAOMTK.COM.ipa"
        else:
            continue

    seen_names.add(name)
    version = str(item.get("version", "1.0"))
    size_str = str(item.get("size", "100 MB"))
    icon = item.get("iconURL") or item.get("icon") or item.get("image") or "https://ashtemobile.site/logo.png"
    bundle = item.get("bundleIdentifier") or item.get("bundle") or f"com.ashtemobile.{hashlib.md5(name.encode()).hexdigest()[:6]}"
    
    numeric_id = int(hashlib.md5(bundle.encode()).hexdigest()[:8], 16) % (10**9)

    app_entry = {
        "id": numeric_id,
        "name": name,
        "version": version,
        "size": size_str,
        "icon": icon,
        "badge": "",
        "type": "games",
        "install_url": download_url,
        "download_url": download_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "IPAOMTK Official",
        "localizedDescription": item.get("description", "Extracted directly from ipaomtk.com"),
        "iconURL": icon,
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "localizedDescription": None,
                "downloadURL": download_url,
                "size": 100 * 1024 * 1024,
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
    apps_list.append(app_entry)

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

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"\nSUCCESS! Saved {len(apps_list)} games from ipaomtk.com into {json_file}.")
print("=== FINISHED ===")
