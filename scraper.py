import hashlib
import json
from datetime import datetime

print("=== ASHTE MOBILE: COMPLETE IPAOMTK CATALOG GENERATOR ===")

json_file = "ashtemobile94.json"

# گەورەترین لیستی یاری و ئەپەکانی ڕەسەنی IPAOMTK لەگەڵ لۆگۆ و زانیاری تەواو
complete_catalog = [
    {
        "name": "Secret of Mana",
        "version": "3.3.0",
        "size": "187.78 MB",
        "slug": "secret-of-mana",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/09/Secret-of-Mana-IPA-v3.3.0-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "Clay Jam Classic",
        "version": "1.5",
        "size": "181.62 MB",
        "slug": "clay-jam-classic",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/09/Clay-Jam-Classic-IPA-v1.5-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "MIST: Offline Zombie Survival",
        "version": "1.8.13",
        "size": "594.98 MB",
        "slug": "mist-offline-zombie-survival",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/09/MIST-Offline-Zombie-Survival-IPA-v1.8.13-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "My Sushi Story",
        "version": "5.6.0",
        "size": "464.2 MB",
        "slug": "my-sushi-story",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/09/My-Sushi-Story-IPA-v5.6.0-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "PreCats! -Idle Cat Raising",
        "version": "2.1.32",
        "size": "277 MB",
        "slug": "precats-idle-cat-raising",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/09/PreCats-Idle-Cat-Raising-IPA-v2.1.32-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "Knock Knock: Room Defense",
        "version": "10000.0.70",
        "size": "536.04 MB",
        "slug": "knock-knock-room-defense",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/09/Knock-Knock-Room-Defense-IPA-v10000.0.70-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "Cafe SuperMart Simulator",
        "version": "1.0",
        "size": "154.22 MB",
        "slug": "cafe-supermart-simulator",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/09/Cafe-SuperMart-Simulator-IPA-v1.0-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "Merge Sweets",
        "version": "91.3",
        "size": "474.64 MB",
        "slug": "merge-sweets",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/09/Merge-Sweets-IPA-v91.3-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "GTA San Andreas",
        "version": "2.2.21",
        "size": "1.5 GB",
        "slug": "grand-theft-auto-san-andreas-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/Grand-Theft-Auto-San-Andreas-gta-ipa-150x150.jpg"
    },
    {
        "name": "Car Parking Multiplayer 2",
        "version": "1.4.2",
        "size": "1.6 GB",
        "slug": "car-parking-multiplayer-2",
        "icon": "https://ipaomtk.com/wp-content/uploads/2024/07/car-parking-multiplayer-2-ipa-v4-9-7-unlimited-cash-unlimited-coins-ios-appstore-icon-150x150.jpg"
    },
    {
        "name": "8 Ball Pool",
        "version": "56.29.2",
        "size": "105 MB",
        "slug": "8-ball-pool",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/download-8-ball-pool-1-150x150.png"
    },
    {
        "name": "Toca Boca World",
        "version": "1.138.1",
        "size": "703.74 MB",
        "slug": "toca-boca-world",
        "icon": "https://ipaomtk.com/wp-content/uploads/2024/12/Toca-Boca-World-150x150.webp"
    },
    {
        "name": "Nulls Brawl IPA",
        "version": "68.279",
        "size": "533 MB",
        "slug": "nulls-brawl",
        "icon": "https://ipaomtk.com/wp-content/uploads/2024/03/Nulls-Brawl-logo-150x150.jpg"
    },
    {
        "name": "Shadow Fight 2",
        "version": "2.46.0",
        "size": "173.33 MB",
        "slug": "shadow-fight-2-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/shadow-fight-2-ipa-v2-46-0-unlimited-all-max-level-ios-appstore-icon-150x150.jpg"
    },
    {
        "name": "Roblox",
        "version": "2.737.1581",
        "size": "232.8 MB",
        "slug": "roblox-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/03/Roblox-IPA-LOGO-150x150.png"
    },
    {
        "name": "PUBG MOBILE",
        "version": "4.6.0",
        "size": "3.6 GB",
        "slug": "pubg-mobile-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/07/pubg-mobile-ipa-v4-5-0-menu-esp-ios-appstore-icon-1-150x150.jpg"
    },
    {
        "name": "Subway Surfers",
        "version": "3.69.0",
        "size": "150 MB",
        "slug": "subway-surfers",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/2024-09-19-1.30.25-AM-150x150.jpg"
    },
    {
        "name": "Gunfire Reborn IPA",
        "version": "1.0.26",
        "size": "1.7 GB",
        "slug": "gunfire-reborn-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/11/download-gunfire-reborn-150x150.png"
    },
    {
        "name": "Foundation: Galactic Frontier",
        "version": "1.1.153",
        "size": "3298.58 MB",
        "slug": "foundation-galactic-frontier",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/07/Foundation-Galactic-Frontier-IPA-v1.1.77-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "Wizardry Variants Daphne",
        "version": "1.37.0",
        "size": "1143.56 MB",
        "slug": "wizardry-variants-daphne",
        "icon": "https://ipaomtk.com/wp-content/uploads/2025/04/Wizardry-Variants-Daphne-150x150.webp"
    },
    {
        "name": "Bowmasters",
        "version": "11.6.3",
        "size": "135.60 MB",
        "slug": "bowmasters-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/11/download-bowmasters-150x150.png"
    },
    {
        "name": "Armada: Warships Legends",
        "version": "4.1.0",
        "size": "688.7 MB",
        "slug": "armada-warships-legends",
        "icon": "https://ipaomtk.com/wp-content/uploads/2026/05/Armada-Warships-Legends-IPA-v3.7.0-Unlocked-For-iOS-featured-image-150x150.jpg"
    },
    {
        "name": "Cats & Soup",
        "version": "5.1.2",
        "size": "250 MB",
        "slug": "cats-and-soup-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/10/Cats-Soup-150x150.jpg"
    },
    {
        "name": "Hole.io",
        "version": "2.52.4",
        "size": "175 MB",
        "slug": "holeio-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/Hole-io-IPA-150x150.png"
    },
    {
        "name": "Skullgirls: Fighting RPG",
        "version": "8.10.2",
        "size": "349.7 MB",
        "slug": "skullgirls-fighting-rpg-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/10/Skullgirls-1-150x150.jpg"
    },
    {
        "name": "CapCut Video Editor",
        "version": "13.9.2",
        "size": "222.56 MB",
        "slug": "capcut-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/CapCut-PRO-ipa-150x150.png"
    },
    {
        "name": "Spotify Music and Podcasts",
        "version": "9.1.78",
        "size": "81.9 MB",
        "slug": "spotify-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/spotify-IPA-150x150.jpg"
    },
    {
        "name": "YouTube",
        "version": "21.35.3",
        "size": "125.11 MB",
        "slug": "youtube-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/2024-09-05-5.24.18-PM-150x150.jpg"
    },
    {
        "name": "TikTok IPA",
        "version": "46.2.0",
        "size": "240 MB",
        "slug": "tiktok-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/TIKTOK-150x150.jpg"
    },
    {
        "name": "Instagram",
        "version": "433.0.0",
        "size": "154.3 MB",
        "slug": "instagram-ipa",
        "icon": "https://ipaomtk.com/wp-content/uploads/2023/02/Instagram-IPA-1-150x150.jpg"
    }
]

apps_list = []

for item in complete_catalog:
    name = item["name"]
    version = item["version"]
    size_str = item["size"]
    slug = item["slug"]
    icon_url = item["icon"]
    
    download_url = f"https://file.ipaomtk.com/{slug}/{slug}-IPAOMTK.COM.ipa"
    numeric_id = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.{slug.replace('-', '').replace('_', '').replace('.', '')}"

    size_bytes = 500 * 1024 * 1024
    try:
        if "GB" in size_str:
            size_bytes = int(float(size_str.replace("GB", "").strip()) * 1024 * 1024 * 1024)
        elif "MB" in size_str:
            size_bytes = int(float(size_str.replace("MB", "").strip()) * 1024 * 1024)
    except:
        pass

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
        "subtitle": "IPAOMTK Official Source",
        "localizedDescription": f"Official {name} IPA extracted from ipaomtk.com catalog.",
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
    print(f" + Added catalog item: {name}")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all games and apps from ipaomtk.com.",
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

print(f"\nSUCCESS! Generated {len(apps_list)} items with official icons into {json_file}.")
