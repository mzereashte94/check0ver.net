import hashlib
import json
import re
import requests
from datetime import datetime

print("=== ASHTE MOBILE: WORDPRESS REST API ALL GAMES SCRAPER ===")

json_file = "ashtemobile94.json"
api_base = "https://ipaomtk.com/wp-json/wp/v2/posts"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

apps_list = []
seen_slugs = set()

page = 1
while True:
    url = f"{api_base}?per_page=100&page={page}"
    try:
        print(f"Fetching WordPress API page {page}...")
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            print(f"Reached end of API pages or status code {res.status_code}.")
            break
            
        posts = res.json()
        if not posts or not isinstance(posts, list):
            break
            
        for post in posts:
            title_raw = post.get('title', {}).get('rendered', '')
            title = re.sub('<.*?>', '', title_raw).strip()
            if not title:
                continue
                
            slug = post.get('slug', '')
            if not slug:
                slug = title.lower().replace(' ', '-').replace(':', '').replace('!', '').replace('(', '').replace(')', '')
                
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            
            # دروستکردنی لینکی ڕەسەن ڕێک لەسەر file.ipaomtk.com
            download_url = f"https://file.ipaomtk.com/{slug}/{slug}-IPAOMTK.COM.ipa"
            icon_url = "https://ipaomtk.com/wp-content/uploads/2026/06/ipaomtk.jpeg"
            
            numeric_id = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16) % (10**9)
            bundle = f"com.ashtemobile.{slug.replace('-', '').replace('_', '').replace('.', '')}"
            
            app_entry = {
                "id": numeric_id,
                "name": title,
                "version": "1.0",
                "size": "300 MB",
                "icon": icon_url,
                "badge": "MOD",
                "type": "games",
                "install_url": download_url,
                "download_url": download_url,
                "bundleIdentifier": bundle,
                "marketplaceID": "",
                "developerName": "AshteMobile",
                "subtitle": "IPAOMTK Direct File Source",
                "localizedDescription": f"Official {title} IPA hosted directly on file.ipaomtk.com.",
                "iconURL": icon_url,
                "tintColor": "#04ecfc",
                "category": "games",
                "screenshots": [],
                "versions": [
                    {
                        "version": "1.0",
                        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                        "localizedDescription": None,
                        "downloadURL": download_url,
                        "size": 300 * 1024 * 1024,
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
            
        print(f"Processed page {page}. Total games collected so far: {len(apps_list)}")
        if len(posts) < 100:
            break
        page += 1
    except Exception as e:
        print(f"Error on page {page}: {e}")
        break

print(f"\nTotal extracted games and apps: {len(apps_list)}")

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

print(f"SUCCESS! Saved {len(apps_list)} games into {json_file}.")
