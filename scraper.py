import hashlib
import json
from datetime import datetime
from playwright.sync_api import sync_playwright

print("=== ASHTE MOBILE: AUTOMATED 253 PAGES IPAOMTK EXTRACTOR ===")

json_file = "ashtemobile94.json"
target_base = "https://ipaomtk.com/games/page/"

raw_games = []
seen_slugs = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        viewport={"width": 390, "height": 844}
    )
    page = context.new_page()

    print("Bypassing Cloudflare and scraping all 253 pages...")
    
    # گەڕان بەناو هەموو پەڕەکانی سایتەکەدا (تا پەڕەی 253)
    for page_num in range(1, 254):
        url = f"{target_base}{page_num}/" if page_num > 1 else "https://ipaomtk.com/games/"
        try:
            page.goto(url, wait_until="networkidle", timeout=25000)
            page.wait_for_timeout(1500)
            
            cards = page.query_selector_all('a.ipaomtk-app-card')
            if not cards:
                break
                
            found_in_page = 0
            for card in cards:
                href = card.get_attribute('href') or ""
                title_elem = card.query_selector('.ipaomtk-card-title')
                name = title_elem.inner_text().strip() if title_elem else ""
                
                if not name:
                    continue
                    
                slug = href.strip('/').split('/')[-1] if href else name.lower().replace(' ', '-')
                if not slug or slug in seen_slugs or slug in ['games', 'page', 'ipaomtk.com']:
                    slug = name.lower().replace(' ', '-').replace(':', '').replace('!', '').replace('(', '').replace(')', '')
                
                if slug in seen_slugs:
                    continue
                seen_slugs.add(slug)
                
                img_elem = card.query_selector('img')
                icon_url = "https://ashtemobile.site/logo.png"
                if img_elem:
                    icon_url = img_elem.get_attribute('src') or img_elem.get_attribute('data-src') or icon_url
                    if icon_url.startswith('/'):
                        icon_url = f"https://ipaomtk.com{icon_url}"
                
                size_str = "300 MB"
                try:
                    meta_span = card.query_selector('.ipaomtk-card-meta span:nth-child(2)')
                    if meta_span:
                        size_str = meta_span.inner_text().strip()
                except:
                    pass

                raw_games.append({
                    "name": name,
                    "slug": slug,
                    "icon": icon_url,
                    "size": size_str
                })
                found_in_page += 1
                
            if page_num % 10 == 0:
                print(f"Scraped page {page_num}... Total games found so far: {len(raw_games)}")
                
            if found_in_page == 0 and page_num > 10:
                break
        except Exception as e:
            break

    browser.close()

print(f"Total unique games collected: {len(raw_games)}. Generating final JSON...")

apps_list = []
for item in raw_games:
    name = item["name"]
    slug = item["slug"]
    icon_url = item["icon"]
    size_str = item["size"]
    
    # دروستکردنی لینکی ڕەسەن ڕێک لەسەر file.ipaomtk.com
    download_url = f"https://file.ipaomtk.com/{slug}/{slug}-IPAOMTK.COM.ipa"
    numeric_id = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.{slug.replace('-', '').replace('_', '').replace('.', '')}"

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
        "version": "1.0",
        "size": size_str if size_str else "300 MB",
        "icon": icon_url,
        "badge": "MOD",
        "type": "games",
        "install_url": download_url,
        "download_url": download_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "IPAOMTK Direct File Source",
        "localizedDescription": f"Official {name} IPA hosted on file.ipaomtk.com.",
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

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all games and apps from file.ipaomtk.com.",
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

print(f"\nSUCCESS! Extracted {len(apps_list)} games with file.ipaomtk.com links into {json_file}.")
