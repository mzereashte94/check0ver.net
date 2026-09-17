import json
import hashlib
from datetime import datetime

print("=== ASHTE MOBILE: COMPLETE IPAOMTK GAMES CATALOG ===")

json_file = "ashtemobile94.json"

# هەموو یارییە فەرمییەکانی ناو سایتی ipaomtk.com لەگەڵ لینکە ڕەسەنەکانیان
all_ipaomtk_games = [
    {
        "name": "Castle Busters",
        "version": "1.18.1",
        "size": "396.62 MB",
        "download_url": "https://file.ipaomtk.com/castle-busters/castle-busters-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/castle-busters.png"
    },
    {
        "name": "Secret of Mana",
        "version": "3.3.0",
        "size": "187.78 MB",
        "download_url": "https://file.ipaomtk.com/secret-of-mana/secret-of-mana-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/secret-of-mana.png"
    },
    {
        "name": "Clay Jam Classic",
        "version": "1.5",
        "size": "181.62 MB",
        "download_url": "https://file.ipaomtk.com/clay-jam-classic/clay-jam-classic-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/clay-jam.png"
    },
    {
        "name": "MIST: Offline Zombie Survival",
        "version": "1.8.13",
        "size": "594.98 MB",
        "download_url": "https://file.ipaomtk.com/mist/mist-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/mist.png"
    },
    {
        "name": "My Sushi Story",
        "version": "5.6.0",
        "size": "464.2 MB",
        "download_url": "https://file.ipaomtk.com/my-sushi-story/my-sushi-story-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/sushi-story.png"
    },
    {
        "name": "PreCats! - Cat Raising",
        "version": "1.0",
        "size": "200.0 MB",
        "download_url": "https://file.ipaomtk.com/precats/precats-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/precats.png"
    },
    {
        "name": "BitLife - Life Simulator",
        "version": "3.14",
        "size": "350.0 MB",
        "download_url": "https://file.ipaomtk.com/bitlife/bitlife-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/bitlife.png"
    },
    {
        "name": "Grand Theft Auto: San Andreas",
        "version": "2.10",
        "size": "1.5 GB",
        "download_url": "https://file.ipaomtk.com/gta-sa/gta-sa-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/gta-sa.png"
    },
    {
        "name": "Minecraft",
        "version": "1.20.0",
        "size": "850.0 MB",
        "download_url": "https://file.ipaomtk.com/minecraft/minecraft-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/minecraft.png"
    },
    {
        "name": "Car Parking Multiplayer",
        "version": "4.8.4",
        "size": "950.0 MB",
        "download_url": "https://file.ipaomtk.com/car-parking/car-parking-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/car-parking.png"
    },
    {
        "name": "Stumble Guys",
        "version": "0.55",
        "size": "180.0 MB",
        "download_url": "https://file.ipaomtk.com/stumble-guys/stumble-guys-IPAOMTK.COM.ipa",
        "icon": "https://ipaomtk.com/uploads/icons/stumble-guys.png"
    }
]

apps_list = []

for item in all_ipaomtk_games:
    name = item["name"]
    version = item["version"]
    size_str = item["size"]
    download_url = item["download_url"]
    icon_url = item["icon"]
    
    numeric_id = int(hashlib.md5(name.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.{name.lower().replace(' ', '').replace(':', '').replace('!', '').replace('-', '')}"
    
    app_entry = {
        "id": numeric_id,
        "name": name,
        "version": version,
        "size": size_str,
        "icon": icon_url,
        "badge": "MOD",
        "type": "games",
        "install_url": download_url,
        "download_url": download_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "IPAOMTK Official Game",
        "localizedDescription": f"Official {name} IPA extracted from ipaomtk.com games library.",
        "iconURL": icon_url,
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "localizedDescription": None,
                "downloadURL": download_url,
                "size": 500 * 1024 * 1024,
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
    print(f" + Added Game with Icon: {name}")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all of my games from IPAOMTK.",
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

print(f"\nSUCCESS! Saved {len(apps_list)} pure IPAOMTK games with icons into {json_file}.")
print("=== FINISHED ===")
