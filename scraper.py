import json
import hashlib
import re
from datetime import datetime
from curl_cffi import requests
from bs4 import BeautifulSoup

print("=== ASHTE MOBILE: DIRECT IPAOMTK GAMES EXTRACTOR ===")

json_file = "ashtemobile94.json"
target_url = "https://ipaomtk.com/games/"

apps_list = []
seen_urls = set()

print(f"Bypassing Cloudflare and fetching from {target_url}...")

try:
    response = requests.get(target_url, impersonate="chrome120", timeout=30)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        for a in links:
            href = a['href']
            if "/games/" in href or "/app/" in href or "/ipa/" in href:
                app_url = href if href.startswith('http') else f"https://ipaomtk.com{href}"
                if app_url in seen_urls or app_url == target_url:
                    continue
                seen_urls.add(app_url)
                
                try:
                    app_res = requests.get(app_url, impersonate="chrome120", timeout=10)
                    if app_res.status_code == 200:
                        app_soup = BeautifulSoup(app_res.text, 'html.parser')
                        
                        title_tag = app_soup.find('h1') or app_soup.find('h2')
                        name = title_tag.get_text(strip=True) if title_tag else "Unknown Game"
                        
                        ipa_link = ""
                        for tag in app_soup.find_all(['a', 'source'], href=True):
                            link_val = tag.get('href', '')
                            if '.ipa' in link_val or 'file.ipaomtk.com' in link_val:
                                ipa_link = link_val
                                break
                        
                        if not ipa_link:
                            found = re.search(r'(https?://[^\s\'"<>]+?\.ipa)', app_res.text)
                            if found:
                                ipa_link = found.group(1)
                        
                        if ipa_link:
                            numeric_id = int(hashlib.md5(app_url.encode()).hexdigest()[:8], 16) % (10**9)
                            bundle = f"com.ashtemobile.app{numeric_id}"
                            
                            app_entry = {
                                "id": numeric_id,
                                "name": name,
                                "version": "1.0",
                                "size": "Unknown",
                                "icon": "https://ashtemobile.site/logo.png",
                                "badge": "",
                                "type": "games",
                                "install_url": ipa_link,
                                "download_url": ipa_link,
                                "bundleIdentifier": bundle,
                                "marketplaceID": "",
                                "developerName": "AshteMobile",
                                "subtitle": "IPAOMTK Direct Game",
                                "localizedDescription": f"Extracted from {app_url}",
                                "iconURL": "https://ashtemobile.site/logo.png",
                                "tintColor": "#04ecfc",
                                "category": "games",
                                "screenshots": [],
                                "versions": [
                                    {
                                        "version": "1.0",
                                        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                                        "localizedDescription": None,
                                        "downloadURL": ipa_link,
                                        "size": 100 * 1024 * 1024,
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
                except Exception as inner_e:
                    pass
                    
except Exception as e:
    print(f"Main scraping error: {e}")

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

print(f"\nSUCCESS! Successfully saved {len(apps_list)} games from IPAOMTK into {json_file}.")
print("=== FINISHED ===")
