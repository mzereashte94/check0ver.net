import hashlib
import json
import requests
import concurrent.futures
from datetime import datetime
from bs4 import BeautifulSoup

print("=== ASHTE MOBILE: FULL 253 PAGES IPAOMTK SCRAPER ===")

json_file = "ashtemobile94.json"
base_url = "https://ipaomtk.com/games/page/"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

raw_games = []
seen_slugs = set()

print("Fetching all games from pagination (1 to 253)...")

for page in range(1, 254):
    url = f"{base_url}{page}/" if page > 1 else "https://ipaomtk.com/games/"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('a', href=True)
            found_in_page = 0
            
            for card in cards:
                href = card['href']
                if '/games/' in href or '-ipa' in href or 'slug' in href:
                    slug = href.strip('/').split('/')[-1]
                    if not slug or slug in ['games', 'page', 'ipaomtk.com'] or slug in seen_slugs:
                        continue
                    
                    title_elem = card.find(['h3', 'h2', 'span'])
                    name = title_elem.get_text(strip=True) if title_elem else slug.replace('-', ' ').title()
                    
                    if len(name) < 2 or name in ["View All", "Download", "Details", "Home"]:
                        continue
                        
                    seen_slugs.add(slug)
                    
                    img_elem = card.find('img')
                    icon_url = "https://ashtemobile.site/logo.png"
                    if img_elem:
                        icon_url = img_elem.get('src') or img_elem.get('data-src') or icon_url
                        if icon_url.startswith('/'):
                            icon_url = f"https://ipaomtk.com{icon_url}"

                    raw_games.append({
                        "name": name,
                        "slug": slug,
                        "icon": icon_url
                    })
                    found_in_page += 1
            
            if page % 10 == 0:
                print(f"Scraped up to page {page}... Found {len(raw_games)} games so far.")
                
            if found_in_page == 0 and page > 10:
                break
        else:
            break
    except Exception as e:
        pass

print(f"Total unique games found: {len(raw_games)}. Generating JSON...")

apps_list = []

def process_game(item):
    name = item["name"]
    slug = item["slug"]
    icon_url = item["icon"]
    
    download_url = f"https://file.ipaomtk.com/{slug}/{slug}-IPAOMTK.COM.ipa"
    numeric_id = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.{slug.replace('-', '').replace('_', '')}"

    return {
        "id": numeric_id,
        "name": name,
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
        "subtitle": "IPAOMTK Game",
        "localizedDescription": f"Extracted from ipaomtk.com games library.",
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

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(process_game, raw_games)
    for res in results:
        if res:
            apps_list.append(res)

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all games from ipaomtk.com.",
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

print(f"\nSUCCESS! Extracted and saved {len(apps_list)} games into {json_file}.")
