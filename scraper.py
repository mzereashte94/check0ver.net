import hashlib
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

print("=== ASHTE MOBILE: HTML PARSER FOR IPAOMTK ===")

json_file = "ashtemobile94.json"
target_url = "https://ipaomtk.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
}

apps_list = []
seen_slugs = set()

try:
    print(f"Fetching from {target_url}...")
    res = requests.get(target_url, headers=headers, timeout=15)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        cards = soup.find_all('a', href=True)
        
        for card in cards:
            href = card['href']
            if any(x in href for x in ['-ipa', 'secret-of-mana', 'clay-jam', 'mist', 'sushi', 'precats', 'gta', 'minecraft', 'knock-knock', 'cafe-supermart', 'merge-sweets']):
                title_elem = card.find(['h3', 'h2', 'span'])
                name = title_elem.get_text(strip=True) if title_elem else ""
                
                if not name or len(name) < 2 or name in ["View All", "Download", "Details"]:
                    continue
                    
                slug = href.strip('/').split('/')[-1]
                if not slug or slug in seen_slugs:
                    continue
                seen_slugs.add(slug)
                
                img_elem = card.find('img')
                icon_url = "https://ashtemobile.site/logo.png"
                if img_elem:
                    icon_url = img_elem.get('src') or img_elem.get('data-src') or icon_url
                    if icon_url.startswith('/'):
                        icon_url = f"https://ipaomtk.com{icon_url}"

                download_url = f"https://file.ipaomtk.com/{slug}/{slug}-IPAOMTK.COM.ipa"
                numeric_id = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16) % (10**9)
                bundle = f"com.ashtemobile.{slug.replace('-', '').replace('_', '')}"

                app_entry = {
                    "id": numeric_id,
                    "name": name,
                    "version": "1.0",
                    "size": "250 MB",
                    "icon": icon_url,
                    "badge": "MOD",
                    "type": "games",
                    "install_url": download_url,
                    "download_url": download_url,
                    "bundleIdentifier": bundle,
                    "marketplaceID": "",
                    "developerName": "AshteMobile",
                    "subtitle": "IPAOMTK Parsed Game",
                    "localizedDescription": f"Extracted from ipaomtk.com via HTML parser.",
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
                print(f" + Parsed Game: {name}")

except Exception as e:
    print(f"Parsing error: {e}")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all of my games from ipaomtk.com.",
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

print(f"\nSUCCESS! Parsed and saved {len(apps_list)} games into {json_file}.")
