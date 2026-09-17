import json
import requests
import hashlib
from datetime import datetime

print("=== ASHTE MOBILE: FETCHING PERMANENT GITHUB APPS ===")

# ئەو سەرچاوانەی کە لینکەکانیان هەمیشەیین و هی گیت هابن
sources = [
    "https://raw.githubusercontent.com/swaggyP36000/TrollStore-IPAs/main/apps.json",
    "https://raw.githubusercontent.com/qnblackcat/AltStore/main/apps.json"
]

apps_list = []
existing_names = set()

print("1. Fetching apps from reliable open-source libraries...")

for url in sources:
    try:
        print(f" -> Fetching from {url}...")
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            data = res.json()
            for app in data.get("apps", []):
                name = app.get("name", "Unknown")
                
                # بۆ ئەوەی ئەپی دووبارە نەچێتە ناو فایلەکەتەوە
                if name in existing_names:
                    continue
                    
                download_url = app.get("downloadURL", "")
                # تەنها ئەو لینکانە وەردەگرین کە فایلی ڕاستەوخۆی .ipa ن
                if not download_url.endswith(".ipa"):
                    continue
                    
                version = app.get("version", "1.0")
                size = app.get("size", 50000000)
                size_str = f"{round(size / (1024*1024), 2)} MB"
                icon = app.get("iconURL", "https://ashtemobile.site/logo.png")
                bundle = app.get("bundleIdentifier", f"com.ashte.{name.replace(' ', '')}")
                desc = app.get("localizedDescription", "Awesome app.")
                
                # دروستکردنی ئایدی ژمارەیی
                numeric_id = int(hashlib.md5(bundle.encode()).hexdigest()[:8], 16) % (10**9)

                # دروستکردنی فۆرماتەکە ڕێک وەکو ئەوەی خۆت دەتەوێت
                new_app = {
                    "id": numeric_id,
                    "name": name,
                    "version": version,
                    "size": size_str,
                    "icon": icon,
                    "badge": "",
                    "type": "apps",
                    "install_url": download_url,
                    "download_url": download_url,
                    "bundleIdentifier": bundle,
                    "marketplaceID": "",
                    "developerName": app.get("developerName", "AshteMobile"),
                    "subtitle": "Safe & Permanent",
                    "localizedDescription": desc,
                    "iconURL": icon,
                    "tintColor": app.get("tintColor", "#04ecfc"),
                    "category": "apps",
                    "screenshots": app.get("screenshotURLs", []),
                    "versions": [
                        {
                            "version": version,
                            "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                            "localizedDescription": None,
                            "downloadURL": download_url,
                            "size": size,
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
                
                apps_list.append(new_app)
                existing_names.add(name)
                print(f"   + Added Safe App: {name}")
    except Exception as e:
        print(f"Error fetching from {url}: {e}")

# ڕێکخستنی فایلی کۆتایی JSON
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

print(f"\nDone! Extracted {len(apps_list)} PERMANENT .ipa URLs directly into {output_filename}.")
print("=== FINISHED ===")
