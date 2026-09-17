import hashlib
import json
import re
import requests
import concurrent.futures

# بەکارهێنانی هەمان بنەما بۆ سایتی ipaomtk.com
base_url = "https://ipaomtk.com/games/"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

print("1. Fetching games catalog from ipaomtk.com...")
raw_apps = []

try:
    response = requests.get(base_url, headers=headers, timeout=15)
    if response.status_code == 200:
        # گەڕان بەدوای داتای نێو سایتەکە یان لینکەکان
        links = re.findall(r'href=["\'](/games/[^"\']+|/app/[^"\']+)["\']', response.text)
        raw_apps = list(set(links))
except Exception as e:
    print(f"Error fetching base: {e}")

print(f"Found {len(raw_apps)} items. Extracting direct .ipa files...")

def get_real_ipa(path):
    app_url = f"https://ipaomtk.com{path}" if path.startswith('/') else path
    
    # دروستکردنی ناوی یارییەکە لەسەر بنەمای پدسەکە
    parts = path.split('/')
    raw_name = parts[-2] if len(parts) >= 2 and parts[-2] else "Game"
    name = raw_name.replace('-', ' ').replace('_', ' ').title()
    
    final_ipa_url = f"https://file.ipaomtk.com/{raw_name}/{raw_name}-IPAOMTK.COM.ipa"
    image_url = "https://ashtemobile.site/logo.png"
    
    try:
        res = requests.get(app_url, headers=headers, timeout=5)
        if res.status_code == 200:
            # گەڕان بەدوای لینکی ڕەسەنی .ipa لەناو پەڕەکەدا
            found_ipa = re.search(r'(https?://file\.ipaomtk\.com/[^\s\'"<>]+?\.ipa)', res.text)
            if found_ipa:
                final_ipa_url = found_ipa.group(1)
            
            # گەڕان بەدوای لۆگۆ یان وێنەی یارییەکە
            found_img = re.search(r'src=["\']([^"\']+\.(png|jpg|webp))["\']', res.text)
            if found_img and "logo" not in found_img.group(1):
                img_path = found_img.group(1)
                image_url = img_path if img_path.startswith('http') else f"https://ipaomtk.com{img_path}"
    except:
        pass

    numeric_id = int(hashlib.md5(app_url.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.app{numeric_id}"

    return {
        "id": numeric_id,
        "name": name,
        "version": "1.0",
        "size": "250.0 MB",
        "icon": image_url,
        "badge": "MOD",
        "type": "games",
        "install_url": final_ipa_url,
        "download_url": final_ipa_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "IPAOMTK Game",
        "localizedDescription": "Extracted from ipaomtk.com via AshteMobile Scraper.",
        "iconURL": image_url,
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": "1.0",
                "date": "2026-09-17T00:00:00+00:00",
                "localizedDescription": None,
                "downloadURL": final_ipa_url,
                "size": 250 * 1024 * 1024,
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

apps_list = []

# بەکارهێنانی خێراییە شێتانەکەی ThreadPoolExecutor بۆ دەرهێنانی لینکەکان
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(get_real_ipa, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

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

print(f"Done! Extracted {len(apps_list)} games into {output_filename}.")
