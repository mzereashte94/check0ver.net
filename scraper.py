import json
import hashlib
from datetime import datetime

print("=== ASHTE MOBILE: PURE IPAOMTK GAMES INJECTOR ===")

json_file = "ashtemobile94.json"

# تەنها و تەنها یارییەکانی سایتی ipaomtk.com با لینکە ڕەسەنەکانی خۆیان (file.ipaomtk.com)
ipaomtk_games = [
    {
        "name": "Castle Busters",
        "version": "1.18.1",
        "size": "396.62 MB",
        "download_url": "https://file.ipaomtk.com/castle-busters/castle-busters-IPAOMTK.COM.ipa"
    },
    {
        "name": "Secret of Mana",
        "version": "3.3.0",
        "size": "187.78 MB",
        "download_url": "https://file.ipaomtk.com/secret-of-mana/secret-of-mana-IPAOMTK.COM.ipa"
    },
    {
        "name": "Clay Jam Classic",
        "version": "1.5",
        "size": "181.62 MB",
        "download_url": "https://file.ipaomtk.com/clay-jam-classic/clay-jam-classic-IPAOMTK.COM.ipa"
    },
    {
        "name": "MIST: Offline Zombie Survival",
        "version": "1.8.13",
        "size": "594.98 MB",
        "download_url": "https://file.ipaomtk.com/mist/mist-IPAOMTK.COM.ipa"
    },
    {
        "name": "My Sushi Story",
        "version": "5.6.0",
        "size": "464.2 MB",
        "download_url": "https://file.ipaomtk.com/my-sushi-story/my-sushi-story-IPAOMTK.COM.ipa"
    },
    {
        "name": "PreCats! - Cat Raising",
        "version": "1.0",
        "size": "200.0 MB",
        "download_url": "https://file.ipaomtk.com/precats/precats-IPAOMTK.COM.ipa"
    },
    {
        "name": "BitLife - Life Simulator",
        "version": "3.14",
        "size": "350.0 MB",
        "download_url": "https://file.ipaomtk.com/bitlife/bitlife-IPAOMTK.COM.ipa"
    }
]

apps_list = []

for item in ipaomtk_games:
    name = item["name"]
    version = item["version"]
    size_str = item["size"]
    download_url = item["download_url"]
    
    numeric_id = int(hashlib.md5(name.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.{name.lower().replace(' ', '').replace(':', '').replace('!', '').replace('-', '')}"
    
    app_entry = {
        "id": numeric_id,
        "name": name,
        "version": version,
        "size": size_str,
        "icon": "https://ashtemobile.site/logo.png",
        "badge": "MOD",
        "type": "games",
        "install_url": download_url,
        "download_url": download_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "IPAOMTK Official",
        "localizedDescription": "Extracted directly from ipaomtk.com games library.",
        "iconURL": "https://ashtemobile.site/logo.png",
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "localizedDescription": None,
                "downloadURL": download_url,
                "size": 400 * 1024 * 1024,
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
    print(f" + Added IPAOMTK Game: {name}")

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

print(f"\nSUCCESS! Saved {len(apps_list)} pure IPAOMTK games into {json_file}.")
print("=== FINISHED ===")
