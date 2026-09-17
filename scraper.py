import json
import requests
import hashlib
from datetime import datetime

print("=== ASHTE MOBILE: EXTRACTING IPAOMTK STYLE APPS ===")

# هێنانی داتا لە سەرچاوە فەرمی و کاراکانەوە کە هەمان ناوەڕۆکی IPAOMTK تێدایە
source_url = "https://raw.githubusercontent.com/swaggyP36000/TrollStore-IPAs/main/apps.json"

apps_list = []

try:
    print(f"Fetching apps...")
    res = requests.get(source_url, timeout=15)
    if res.status_code == 200:
        data = res.json()
        for app in data.get("apps", []):
            name = app.get("name", "Unknown App")
            download_url = app.get("downloadURL", "")
            
            if not download_url.lower().endswith(".ipa"):
                continue
                
            version = app.get("version", "1.0")
            size_bytes = app.get("size", 50 * 1024 * 1024)
            size_mb = f"{round(size_bytes / (1024 * 1024), 2)} MB"
            icon = app.get("iconURL", "https://ashtemobile.site/logo.png")
            bundle = app.get("bundleIdentifier", f"com.ashtemobile.{hashlib.md5(name.encode()).hexdigest()[:6]}")
            
            numeric_id = int(hashlib.md5(bundle.encode()).hexdigest()[:8], 16) % (10**9)

            new_app = {
                "id": numeric_id,
                "name": name,
                "version": version,
                "size": size_mb,
                "icon": icon,
                "badge": "",
                "type": "games",
                "install_url": download_url,
                "download_url": download_url,
                "bundleIdentifier": bundle,
                "marketplaceID": "",
                "developerName": "AshteMobile",
                "subtitle": "IPAOMTK Alternative",
                "localizedDescription": "High quality IPA extracted for Ashtemobile.",
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
            
            apps_list.append(new_app)
            print(f" + Added: {name}")
            
except Exception as e:
    print(f"Error: {e}")

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

with open("ashtemobile94.json", "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"\nSUCCESS! Saved {len(apps_list)} working apps to ashtemobile94.json")
