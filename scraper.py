import hashlib
import json
from datetime import datetime

print("=== ASHTE MOBILE: EXACT FILE.IPAOMTK.COM GENERATOR ===")

json_file = "ashtemobile94.json"

# هەموو یارییەکان کە ڕاستەوخۆ لەسەر فۆرماتی file.ipaomtk.com کار دەکەن
games_library = [
    {"name": "Grand Theft Auto: San Andreas", "version": "2.10", "size": "1.5 GB", "slug": "gta-sa", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple122/v4/58/63/0f/58630f9a-7359-5f12-07a5-c2cf8ef5733f/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Minecraft", "version": "1.20.0", "size": "850.0 MB", "slug": "minecraft", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/4a/5b/42/4a5b42cf-3d6d-6d35-3b98-d1d78a9c2f68/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "BitLife - Life Simulator", "version": "3.14", "size": "350.0 MB", "slug": "bitlife", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/71/34/41/713441a1-8742-1e96-601e-c15112423bc2/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "MIST: Offline Zombie Survival", "version": "1.8.13", "size": "594.98 MB", "slug": "mist", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/e5/23/94/e52394f0-4a87-1934-2e21-5a550d51cb2c/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Car Parking Multiplayer", "version": "4.8.4", "size": "950.0 MB", "slug": "car-parking", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple126/v4/a7/6b/a5/a76ba5a9-e85d-8b01-3142-6a68fbe15a51/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Secret of Mana", "version": "3.3.0", "size": "187.78 MB", "slug": "secret-of-mana", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple112/v4/9c/6d/81/9c6d8142-5f65-276e-51c6-cf8813bc5e98/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Clay Jam Classic", "version": "1.5", "size": "181.62 MB", "slug": "clay-jam-classic", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple114/v4/83/8f/c3/838fc32b-3e5f-14a1-b841-3b7c35bc7a77/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "My Sushi Story", "version": "5.6.0", "size": "464.2 MB", "slug": "my-sushi-story", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/91/2a/39/912a39a7-4c32-b7e6-12c8-11f8e134b223/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "PreCats! - Cat Raising", "version": "1.0", "size": "200.0 MB", "slug": "precats", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/31/5b/c2/315bc215-28b1-36bc-76e2-218451b62383/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Castle Busters", "version": "1.18.1", "size": "396.62 MB", "slug": "castle-busters", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple122/v4/1b/2d/3a/1b2d3a95-8e7c-2b63-146f-c1f3c3a9f5d1/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Stumble Guys", "version": "0.55", "size": "180.0 MB", "slug": "stumble-guys", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/6b/5a/8f/6b5a8f42-4f05-1a86-7e3f-a38b1f516d21/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Bully: Anniversary Edition", "version": "1.0.f", "size": "2.4 GB", "slug": "bully", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple122/v4/c3/82/f1/c382f1b8-3f85-45d6-d7e1-b4f738a1a115/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Terraria", "version": "1.4.4", "size": "320.0 MB", "slug": "terraria", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple112/v4/94/a3/b5/94a3b5b1-0e19-f55c-15a6-43b91c4d9223/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Limbo", "version": "1.2", "size": "140.0 MB", "slug": "limbo", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple114/v4/28/73/45/28734563-0f73-2b21-4b13-b232679f2911/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Among Us", "version": "2023.7.12", "size": "250.0 MB", "slug": "among-us", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/e2/3b/81/e23b8112-6302-39f1-32b1-512c1b238f12/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Roblox", "version": "2.585", "size": "300.0 MB", "slug": "roblox", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/0d/1c/37/0d1c37b8-b807-7422-9853-29a3a14e9f9c/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Clash of Clans", "version": "15.83", "size": "350.0 MB", "slug": "clash-of-clans", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple122/v4/76/89/3f/76893f44-8d48-6a3f-1d42-263a15291244/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "PUBG Mobile", "version": "2.8.0", "size": "1.8 GB", "slug": "pubg", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple126/v4/4c/a3/9b/4ca39b6b-4e8c-8f19-d126-5a3b2f915243/AppIcon-0-1-85-225.png/512x512bb.jpg"},
    {"name": "Subway Surfers", "version": "3.15.0", "size": "220.0 MB", "slug": "subway-surfers", "icon": "https://is1-ssl.mzstatic.com/image/thumb/Purple126/v4/c3/91/51/c3915152-71c1-4821-2e81-9b151f52b311/AppIcon-0-1-85-225.png/512x512bb.jpg"}
]

apps_list = []

for item in games_library:
    name = item["name"]
    version = item["version"]
    size_str = item["size"]
    slug = item["slug"]
    icon_url = item["icon"]
    
    # دروستکردنی لینکی ڕەسەن بە فۆرماتی file.ipaomtk.com/[slug]/[slug]-IPAOMTK.COM.ipa
    download_url = f"https://file.ipaomtk.com/{slug}/{slug}-IPAOMTK.COM.ipa"
    
    numeric_id = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.{slug.replace('-', '')}"

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
        "subtitle": "IPAOMTK Direct Link",
        "localizedDescription": f"Official {name} IPA hosted on file.ipaomtk.com.",
        "iconURL": icon_url,
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": "2026-09-17T00:00:00+00:00",
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
    print(f" + Added: {name} -> {download_url}")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all of my games from file.ipaomtk.com.",
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
            "date": "2026-09-17T00:00:00+00:00",
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

print(f"Done! Successfully generated {len(apps_list)} games with file.ipaomtk.com links into {output_filename}.")
