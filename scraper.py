import json
import requests
import hashlib
from datetime import datetime

print("=== ASHTE MOBILE: FULLY AUTOMATED SCRAPER ===")

json_file = "ashtemobile94.json"

# سەرچاوە کراوە و بڕواپێکراوەکان بۆ هێنانی هەموو یاری و ئەپەکان بە شێوەی ئۆتۆماتیکی
sources = [
    "https://raw.githubusercontent.com/swaggyP36000/TrollStore-IPAs/main/apps.json",
    "https://raw.githubusercontent.com/qnblackcat/AltStore/main/apps.json"
]

apps_list = []
seen_bundles = set()

for url in sources:
    try:
        print(f"Fetching automatically from: {url}")
        res = requests.get(url, timeout=20)
        if res.status_code == 200:
            data = res.json()
            for app in data.get("apps", []):
                name = app.get("name", "Unknown App")
                
                download_url = app.get("downloadURL", "")
                versions = app.get("versions", [])
                if not download_url and versions:
                    download_url = versions[0].get("downloadURL", "")

                if not download_url or not download_url.lower().endswith(".ipa"):
                    continue
                    
                bundle = app.get("bundleIdentifier", f"com.ashtemobile.{hashlib.md5(name.encode()).hexdigest()[:6]}")
                if bundle in seen_bundles:
                    continue
                seen_bundles.add(bundle)

                version = app.get("version", (versions[0].get("version", "1.0") if versions else "1.0"))
                size_bytes = app.get("size", (versions[0].get("size", 50 * 1024 * 1024) if versions else 50 * 1024 * 1024))
                size_mb = f"{round(size_bytes / (1024 * 1024), 2)} MB"
                icon = app.get("iconURL", "https://ashtemobile.site/logo.png")
                desc = app.get("localizedDescription", "Automatically fetched game for Ashtemobile.")
                numeric_id = int(hashlib.md5(bundle.encode()).hexdigest()[:8], 16) % (10**9)

                app_entry = {
                    "id": numeric_id,
                    "name": name,
                    "version": version,
                    "size": size_mb,
                    "icon": icon,
                    "badge": "NEW",
                    "type": "games",
                    "install_url": download_url,
                    "download_url": download_url,
                    "bundleIdentifier": bundle,
                    "marketplaceID": "",
                    "developerName": "AshteMobile",
                    "subtitle": "Auto Fetched",
                    "localizedDescription": desc,
                    "iconURL": icon,
                    "tintColor": "#04ecfc",
                    "category": "games",
                    "screenshots": app.get("screenshotURLs", []),
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
                        "privacy": {
                            "NSUserTrackingUsageDescription": "Your data will be used to deliver personalized ads to you."
                        }
                    },
                    "patreon": [],
                }
                apps_list.append(app_entry)
                print(f" + Auto-extracted: {name}")
    except Exception as e:
        print(f"Error: {e}")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all of my games.",
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

print(f"\nSUCCESS! Automatically fetched {len(apps_list)} games into {json_file}.")
print("=== FINISHED ===")
