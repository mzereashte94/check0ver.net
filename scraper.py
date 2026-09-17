import json
import os
import hashlib
from datetime import datetime
from playwright.sync_api import sync_playwright

print("=== ASHTE MOBILE: PLAYWRIGHT NETWORK INTERCEPTOR ===")

json_file = "ashtemobile94.json"
found_apps = []

# ئامادەکردنی بەشی سەرەوەی JSONـەکە ڕێک وەکو ئەوەی ناردبووت
data = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Here you'll find all of my apps.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "patreonURL": "https://ashtemobile.site/Ashtemobile.json",
    "tintColor": "#ff007f",
    "featuredApps": [],
    "headerURL": "https://ashtemobile.site/logo.png",
    "apps": [],
    "news": [
        {
            "title": "Instagram",
            "identifier": "news_kwuwharinc",
            "caption": "Ashtemobile",
            "date": "2026-08-28T16:13:42+00:00",
            "tintColor": "#ff007f",
            "imageURL": "https://ashtemobile.site/logo.png",
            "notify": True,
            "url": "https://www.instagram.com/ashtemobile",
            "appID": None
        },
        {
            "title": "Telegram",
            "identifier": "news_l2keyetzkn",
            "caption": "Ashtemobile",
            "date": "2026-08-28T16:13:42+00:00",
            "tintColor": "#ff007f",
            "imageURL": "https://ashtemobile.site/logo.png",
            "notify": True,
            "url": "https://t.me/ashtemobile",
            "appID": None
        }
    ]
}

def handle_response(response):
    if "json" in response.headers.get("content-type", ""):
        try:
            resp_json = response.json()
            if isinstance(resp_json, dict) and "apps" in resp_json:
                apps = resp_json["apps"]
                if isinstance(apps, list) and len(apps) > 0:
                    print(f" -> Intercepted {len(apps)} apps from hidden API: {response.url}")
                    found_apps.extend(apps)
        except:
            pass

with sync_playwright() as p:
    print("Launching headless browser...")
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    )
    page = context.new_page()

    page.on("response", handle_response)

    print("Navigating to tryipa.com/ipa-library and waiting for JS to execute...")
    page.goto("https://tryipa.com/ipa-library", wait_until="networkidle", timeout=60000)

    page.wait_for_timeout(10000)
    browser.close()

if len(found_apps) > 0:
    print(f"\nProcessing {len(found_apps)} extracted apps into Ashtemobile format...")
    existing_urls = []
    
    for app in found_apps:
        download_url = app.get("downloadURL")
        
        if download_url and str(download_url).endswith(".ipa"):
            if download_url not in existing_urls:
                # وەرگرتنی زانیارییەکان
                name = app.get("name", "Unknown App")
                version = app.get("version", "1.0")
                size_str = str(app.get("size", "50 MB"))
                icon_url = app.get("iconURL", "https://ashtemobile.site/logo.png")
                
                # دروستکردنی ID لە لینکەکەوە
                numeric_id = int(hashlib.md5(download_url.encode()).hexdigest()[:8], 16) % (10**9)
                
                # گۆڕینی قەبارە بۆ بایت (Bytes) بۆ ناو خشتەی versions
                size_bytes = 50 * 1024 * 1024
                try:
                    if "GB" in size_str:
                        size_bytes = int(float(size_str.replace("GB", "").strip()) * 1024 * 1024 * 1024)
                    elif "MB" in size_str:
                        size_bytes = int(float(size_str.replace("MB", "").strip()) * 1024 * 1024)
                except:
                    pass

                # فۆرماتکردنی یارییەکە ڕێک وەکو ئەوەی داوات کردووە
                new_app = {
                    "id": numeric_id,
                    "name": name,
                    "version": version,
                    "size": size_str,
                    "icon": icon_url,
                    "badge": "",
                    "type": "games" if "game" in str(app).lower() else "apps",
                    "install_url": download_url,
                    "download_url": download_url,
                    "bundleIdentifier": f"com.ashtemobile.app{numeric_id}",
                    "marketplaceID": "",
                    "developerName": "AshteMobile",
                    "subtitle": "Awesome App",
                    "localizedDescription": "Downloaded from AshteMobile Source.",
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
                            "buildVersion": None,
                            "minOSVersion": "14.0"
                        }
                    ],
                    "appPermissions": {
                        "entitlements": [],
                        "privacy": {
                            "NSUserTrackingUsageDescription": "Your data will be used to deliver personalized ads to you."
                        }
                    },
                    "patreon": []
                }
                
                data["apps"].append(new_app)
                existing_urls.append(download_url)
                print(f" + Added: {new_app['name']}")

# سەیڤکردنی فایلی JSON بە شێوازی فەرمی
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"\n=== FINISHED! Successfully extracted and formatted {len(data['apps'])} real IPA links. ===")
