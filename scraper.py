import hashlib
import json
import requests
import re
from datetime import datetime

print("=== ASHTE MOBILE: CHECK0VER VIP SCRAPER (.IPA LINKS) ===")

json_file = "ashtemobile94.json"

# کۆدەکانت لێرەدا دابنێ وەکو خۆی
MY_COOKIE = "لێرەدا_کۆدی_Cookie_دابنێ"
MY_XSRF_TOKEN = "لێرەدا_کۆدی_X-XSRF-TOKEN_دابنێ"

headers = {
    "Host": "check0ver.net",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.6.1 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/plain, */*",
    "X-Inertia": "true",
    "X-Inertia-Version": "mimusoft-ipa-check0ver-customer-1.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": MY_COOKIE,
    "X-XSRF-TOKEN": MY_XSRF_TOKEN,
    "Priority": "u=3, i",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

apps_list = []

print("Starting to fetch all games directly from Check0ver API...")

for page in range(1, 165):
    url = f"https://check0ver.net/en/iapps?page={page}"
    try:
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"Stopped or failed at page {page}. Status Code: {response.status_code}")
            break
            
        data = response.json()
        items = data.get("props", {}).get("paginator", {}).get("data", [])
        
        if not items:
            print("No more items found. Scraping finished!")
            break
            
        for item in items:
            name = item.get("name", "Unknown App")
            version = item.get("version", "1.0")
            size_str = item.get("size", "300 MB")
            icon_url = item.get("image", "https://ashtemobile.site/logo.png")
            bundle = item.get("bundle", "com.ashtemobile.app")
            uuid = item.get("uuid", "")
            description = item.get("description", f"Extracted automatically from Check0ver: {name}")
            
            # دروستکردنی ناوی فایلەکە بە خاوێنی
            clean_name = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
            
            # لێرەدا فێڵەکەمان بەکارهێناوە بۆ ئەوەی کۆتاییەکەی ببێت بە .ipa بێ ئەوەی لینکەکە تێکبچێت
            download_url = item.get("downloadURL")
            if not download_url:
                download_url = f"https://check0ver.net/api/iapps/{uuid}/download?file={clean_name}.ipa"
            else:
                if ".ipa" not in download_url:
                    download_url = f"{download_url}?file={clean_name}.ipa"
            
            numeric_id = int(hashlib.md5(uuid.encode()).hexdigest()[:8], 16) % (10**9) if uuid else int(hashlib.md5(name.encode()).hexdigest()[:8], 16) % (10**9)
            
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
                "developerName": "AshteMobile / Check0ver",
                "subtitle": "Check0ver Premium Source",
                "localizedDescription": description,
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
            
        print(f" + Scraped page {page}. Total apps collected: {len(apps_list)}")
        
    except Exception as e:
        print(f"Error on page {page}: {e}")
        break

print(f"\nTotal collected: {len(apps_list)}. Generating JSON file...")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! This catalog is generated directly via VIP API.",
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

print(f"SUCCESS! Finished writing {len(apps_list)} games with .ipa links to {json_file}.")
