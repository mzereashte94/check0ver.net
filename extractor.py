import hashlib
import json
import re
import requests
import time

base_url = (
    "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf&page="
)
# دانانی هێدەری بەهێز بۆ ئەوەی ماڵپەڕەکە گیتهاب بلۆک نەکات
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

apps_list = []

print("Starting safe and reliable extraction...")

for page in range(1, 161):
    url = f"{base_url}{page}"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            match = re.search(r'data-page="([^"]+)"', response.text)
            if match:
                html_escape_decoded = (
                    match.group(1)
                    .replace("&quot;", '"')
                    .replace("&amp;", "&")
                    .replace("&#039;", "'")
                )
                page_data = json.loads(html_escape_decoded)

                paginator = (
                    page_data.get("props", {})
                    .get("paginator", {})
                    .get("data", [])
                )
                if not paginator:
                    print(f"No more apps found at page {page}, stopping.")
                    break

                for app in paginator:
                    name = app.get("name")
                    version = app.get("version", "1.0")
                    size_str = app.get("size", "0 MB")
                    uuid = app.get("uuid")
                    bundle = app.get("bundle", f"com.ashtemobile.{uuid}")
                    image_url = app.get("image", "https://ashtemobile.site/logo.png")
                    updated_at = app.get("updatedAt", "2026-09-15T00:00:00+00:00")

                    # ڕێک ئەو لینکەی کە خۆت داوات کردووە بەبێ داواکاری زیادە
                    download_url = f"https://check0ver.net/en/iapps/{uuid}/download"

                    numeric_id = int(hashlib.md5(uuid.encode()).hexdigest()[:8], 16) % (10**9)

                    size_bytes = 50 * 1024 * 1024
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
                        "icon": image_url if image_url else "https://ashtemobile.site/logo.png",
                        "badge": "",
                        "type": "games",
                        "install_url": download_url,
                        "download_url": download_url,
                        "bundleIdentifier": bundle,
                        "marketplaceID": "",
                        "developerName": "AshteMobile",
                        "subtitle": "Awesome App",
                        "localizedDescription": "Downloaded from AshteMobile Source.",
                        "iconURL": image_url if image_url else "https://ashtemobile.site/logo.png",
                        "tintColor": "#04ecfc",
                        "category": "games",
                        "screenshots": [],
                        "versions": [
                            {
                                "version": version,
                                "date": updated_at,
                                "localizedDescription": None,
                                "downloadURL": download_url,
                                "size": size_bytes,
                                "buildVersion": None,
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
        
        elif response.status_code in [403, 429]:
            print(f"GitHub is temporarily blocked on page {page} (Status: {response.status_code}). Waiting 5 seconds...")
            time.sleep(5)  # چاوەڕێ دەکات تاوەکو لە بلۆک دەردەچێت
        else:
            print(f"Failed to fetch page {page} - Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"Error on page {page}: {e}")

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
            "date": "2026-09-15T00:00:00+00:00",
            "tintColor": "#ff007f",
            "imageURL": "https://ashtemobile.site/logo.png",
            "notify": True,
            "url": "https://www.instagram.com/ashtemobile",
            "appID": None,
        }
    ],
}

output_filename = "ashtemobile94.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"Successfully generated '{output_filename}' with {len(apps_list)} apps!")
