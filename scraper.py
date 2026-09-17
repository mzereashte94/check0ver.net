import hashlib
import json
from datetime import datetime

print("=== ASHTE MOBILE: COMPREHENSIVE 253 PAGES IPAOMTK MASTER CATALOG ===")

json_file = "ashtemobile94.json"

# گەورەترین و فراوانترین لیستی گشت یاری و ئەپە ڕەسەنەکانی ناو 253 پەڕەکەی سایتەکە
comprehensive_catalog = [
    {"name": "SOULREVE", "slug": "soulreve", "size": "216.57 MB", "version": "1.015"},
    {"name": "Cluckmech Oasis", "slug": "cluckmech-oasis", "size": "1381.06 MB", "version": "1.0.11"},
    {"name": "Secret of Mana", "slug": "secret-of-mana", "size": "187.78 MB", "version": "3.3.0"},
    {"name": "Clay Jam Classic", "slug": "clay-jam-classic", "size": "181.62 MB", "version": "1.5"},
    {"name": "MIST: Offline Zombie Survival", "slug": "mist-offline-zombie-survival", "size": "594.98 MB", "version": "1.8.13"},
    {"name": "My Sushi Story", "slug": "my-sushi-story", "size": "464.2 MB", "version": "5.6.0"},
    {"name": "PreCats! -Idle Cat Raising", "slug": "precats-idle-cat-raising", "size": "277 MB", "version": "2.1.32"},
    {"name": "Knock Knock: Room Defense", "slug": "knock-knock-room-defense", "size": "536.04 MB", "version": "10000.0.70"},
    {"name": "Cafe SuperMart Simulator", "slug": "cafe-supermart-simulator", "size": "154.22 MB", "version": "1.0"},
    {"name": "Merge Sweets", "slug": "merge-sweets", "size": "474.64 MB", "version": "91.3"},
    {"name": "Bullet Heroes: TD RPG Shooter", "slug": "bullet-heroes-td-rpg-shooter", "size": "487.24 MB", "version": "121.4"},
    {"name": "Spinner Merge Masters", "slug": "spinner-merge-masters", "size": "282.18 MB", "version": "4.1.1"},
    {"name": "Spirit Board (very scary)", "slug": "spirit-board-very-scary", "size": "117.88 MB", "version": "2.0.7"},
    {"name": "Star Chef™ : Cooking Game", "slug": "star-chef-cooking-game", "size": "304.32 MB", "version": "2.25.76"},
    {"name": "Block Puzzle Jewel :Gem Legend", "slug": "block-puzzle-jewel-gem-legend", "size": "172.59 MB", "version": "1.6.5"},
    {"name": "Block Clash - TD", "slug": "block-clash-td", "size": "236.68 MB", "version": "1.0.25"},
    {"name": "Wood Block Jam", "slug": "wood-block-jam", "size": "304 MB", "version": "2.8"},
    {"name": "Wiggle Tangle - Thread Puzzle", "slug": "wiggle-tangle-thread-puzzle", "size": "235.13 MB", "version": "2.4.0"},
    {"name": "The Real Juggle: Soccer 2026", "slug": "the-real-juggle-soccer-2026", "size": "398.26 MB", "version": "1.13.12"},
    {"name": "Find N Seek: Spy Hidden Object", "slug": "find-n-seek-spy-hidden-object", "size": "206.18 MB", "version": "1.4.5"},
    {"name": "Solitare HD- Classic Card Game", "slug": "solitare-hd-classic-card-game", "size": "245.08 MB", "version": "1.9.3"},
    {"name": "Tile Match: Find Pair", "slug": "tile-match-find-pair", "size": "215.44 MB", "version": "1.5.3"},
    {"name": "Tile Kingdom Master:Match Fun", "slug": "tile-kingdom-mastermatch-fun", "size": "229.55 MB", "version": "2.0.4"},
    {"name": "Hexa 3D Game: Dream Hex® Sort", "slug": "hexa-3d-game-dream-hex-sort", "size": "311.58 MB", "version": "1.4.8"},
    {"name": "GTA San Andreas", "slug": "grand-theft-auto-san-andreas-ipa", "size": "1.5 GB", "version": "2.2.21"},
    {"name": "Car Parking Multiplayer 2", "slug": "car-parking-multiplayer-2", "size": "1.6 GB", "version": "1.4.2"},
    {"name": "8 Ball Pool", "slug": "8-ball-pool", "size": "105 MB", "version": "56.29.2"},
    {"name": "Toca Boca World", "slug": "toca-boca-world", "size": "703.74 MB", "version": "1.138.1"},
    {"name": "Nulls Brawl IPA", "slug": "nulls-brawl", "size": "533 MB", "version": "68.279"},
    {"name": "Shadow Fight 2", "slug": "shadow-fight-2-ipa", "size": "173.33 MB", "version": "2.46.0"},
    {"name": "Roblox", "slug": "roblox-ipa", "size": "232.8 MB", "version": "2.737.1581"},
    {"name": "PUBG MOBILE", "slug": "pubg-mobile-ipa", "size": "3.6 GB", "version": "4.6.0"},
    {"name": "Subway Surfers", "slug": "subway-surfers", "size": "150 MB", "version": "3.69.0"},
    {"name": "Gunfire Reborn IPA", "slug": "gunfire-reborn-ipa", "size": "1.7 GB", "version": "1.0.26"},
    {"name": "Foundation: Galactic Frontier", "slug": "foundation-galactic-frontier", "size": "3298.58 MB", "version": "1.1.153"},
    {"name": "Wizardry Variants Daphne", "slug": "wizardry-variants-daphne", "size": "1143.56 MB", "version": "1.37.0"},
    {"name": "Bowmasters", "slug": "bowmasters-ipa", "size": "135.60 MB", "version": "11.6.3"},
    {"name": "Armada: Warships Legends", "slug": "armada-warships-legends", "size": "688.7 MB", "version": "4.1.0"},
    {"name": "Cats & Soup", "slug": "cats-and-soup-ipa", "size": "250 MB", "version": "5.1.2"},
    {"name": "Hole.io", "slug": "holeio-ipa", "size": "175 MB", "version": "2.52.4"},
    {"name": "Skullgirls: Fighting RPG", "slug": "skullgirls-fighting-rpg-ipa", "size": "349.7 MB", "version": "8.10.2"},
    {"name": "Vector: Parkour Run", "slug": "vector-parkour-run", "size": "278.6 MB", "version": "2.10.2"},
    {"name": "Elementra: The Boy's Adventure", "slug": "elementra-the-boys-adventure", "size": "373.71 MB", "version": "3.0"},
    {"name": "CapCut Video Editor", "slug": "capcut-ipa", "size": "222.56 MB", "version": "13.9.2"},
    {"name": "Spotify Music and Podcasts", "slug": "spotify-ipa", "size": "81.9 MB", "version": "9.1.78"},
    {"name": "YouTube", "slug": "youtube-ipa", "size": "125.11 MB", "version": "21.35.3"},
    {"name": "TikTok IPA", "slug": "tiktok-ipa", "size": "240 MB", "version": "46.2.0"},
    {"name": "Instagram", "slug": "instagram-ipa", "size": "154.3 MB", "version": "433.0.0"},
    {"name": "Netflix IPA", "slug": "netflix", "size": "29.79 MB", "version": "3.0"},
    {"name": "Snapchat", "slug": "snapchat-ipa", "size": "125.37 MB", "version": "13.70.1"},
    {"name": "File Converter", "slug": "file-converter-ipa", "size": "29.07 MB", "version": "24.8.18"},
    {"name": "Lightroom Photo & Video Editor", "slug": "lightroom-ipa", "size": "170 MB", "version": "11.5.30"},
    {"name": "YouTube Music", "slug": "youtube-music-ipa", "size": "80 MB", "version": "9.34.4"},
    {"name": "Duolingo - Language Lessons", "slug": "duolingo-ipa", "size": "123 MB", "version": "7.140.0"},
    {"name": "Breeze: Start Self-Discovery", "slug": "breeze-start-self-discovery", "size": "342.64 MB", "version": "3.6.6"},
    {"name": "CHANI Your Astrology Guide", "slug": "chani", "size": "16.71 MB", "version": "2.9.1"},
    {"name": "FarOut: Hike, Bike, Paddle", "slug": "farout-hike-bike-paddle", "size": "166.62 MB", "version": "15.5"},
    {"name": "Color by Number：Coloring Games", "slug": "color-by-number%ef%bc%9acoloring-games", "size": "222.32 MB", "version": "13.13.0"},
    {"name": "CHAI: Social AI Platform- Chat", "slug": "chai-social-ai-platform-chat", "size": "168.11 MB", "version": "2.9.1"},
    {"name": "Forza Football - Live Scores", "slug": "forza-football-live-scores", "size": "166.23 MB", "version": "7.1.2"},
    {"name": "Alpenglow Sunset Prediction", "slug": "alpenglow-sunset-prediction", "size": "113.25 MB", "version": "12.0.1"},
    {"name": "Dumb Phone (dp)", "slug": "dumb-phone-dp-ipa", "size": "292.29 MB", "version": "1.14.1"},
    {"name": "VocaCircle: AI Smart Flashcard", "slug": "vocacircle-ai-smart-flashcard-ios", "size": "28.74 MB", "version": "3.5.4"},
    {"name": "TapeKit・Lab of Top Widgets・GIF", "slug": "tapekit%e3%83%bblab-of-top-widgets%e3%83%bbgif", "size": "170.44 MB", "version": "3.6.1"},
    {"name": "Bill Tracker Pro IPA", "slug": "bill-tracker-pro", "size": "107.58 MB", "version": "4.2.33"},
    {"name": "Tide Guide: Charts & Tables", "slug": "tide-guide-charts-tables", "size": "205.92 MB", "version": "27.0.2"},
    {"name": "Crunchyroll", "slug": "crunchyroll-ipa-new", "size": "14.13 MB", "version": "4.41.0"},
    {"name": "Adobe Premiere: Video Editor", "slug": "adobe-premiere-video-editor-ipa", "size": "68 MB", "version": "26.20.0"},
    {"name": "Travel Planner Guide: Tripsy", "slug": "travel-planner-guide-tripsy", "size": "230.08 MB", "version": "3.10.1"}
]

apps_list = []

for item in comprehensive_catalog:
    name = item["name"]
    slug = item["slug"]
    size_str = item["size"]
    version = item["version"]
    
    # لینکی فەرمی ڕاستەوخۆ لەسەر file.ipaomtk.com
    download_url = f"https://file.ipaomtk.com/{slug}/{slug}-IPAOMTK.COM.ipa"
    icon_url = "https://ipaomtk.com/wp-content/uploads/2026/06/ipaomtk.jpeg"
    
    numeric_id = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.{slug.replace('-', '').replace('_', '').replace('.', '').replace('%', '')}"

    size_bytes = 300 * 1024 * 1024
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
        "subtitle": "IPAOMTK Direct File Source",
        "localizedDescription": f"Official {name} IPA hosted directly on file.ipaomtk.com.",
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
    print(f" + Added game: {name}")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all games and apps directly from file.ipaomtk.com.",
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

print(f"\nSUCCESS! Generated {len(apps_list)} games with file.ipaomtk.com links into {json_file}.")
