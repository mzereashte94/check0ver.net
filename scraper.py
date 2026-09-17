import hashlib
import json
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

print("=== ASHTE MOBILE: PLAYWRIGHT IPAOMTK EXTRACTOR ===")

json_file = "ashtemobile94.json"
target_site = "https://ipaomtk.com"

found_links = set()

def handle_response(response):
    # پشکنینی هەموو ئەو داتایانەی کە سایتەکە لە پشتەوە دەیهێنێت
    try:
        url = response.url
        if "ipaomtk.com" in url and ("json" in response.headers.get("content-type", "") or "text" in response.headers.get("content-type", "")):
            text = response.text()
            links = re.findall(r'(https?://file\.ipaomtk\.com/[^\s\'"<>]+?\.ipa)', text, re.IGNORECASE)
            for l in links:
                found_links.add(l)
    except:
        pass

with sync_playwright() as p:
    print("Launching headless browser...")
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        viewport={"width": 390, "height": 844}
    )
    page = context.new_page()

    # گوێگرتن لە نێتۆڕکی سایتەکە
    page.on("response", handle_response)

    print(f"Navigating to {target_site} and waiting for JavaScript to load...")
    try:
        page.goto(target_site, wait_until="networkidle", timeout=60000)
        # هێواش هێواش سکرۆڵ دەکەینە خوارەوە بۆ ئەوەی هەموو یارییەکان لۆد ببن
        for _ in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            page.wait_for_timeout(2000)
    except Exception as e:
        print(f"Navigation warning: {e}")

    # گەڕان لەناو HTMLـی سەرەکی پەڕەکەشدا
    content = page.content()
    html_links = re.findall(r'(https?://file\.ipaomtk\.com/[^\s\'"<>]+?\.ipa)', content, re.IGNORECASE)
    for l in html_links:
        found_links.add(l)

    browser.close()

print(f"Total unique IPA links found: {len(found_links)}")

apps_list = []
for link in found_links:
    parts = link.split('/')
    raw_name = parts[-2] if len(parts) >= 2 else "App"
    name = raw_name.replace('-', ' ').replace('_', ' ').title()
    
    numeric_id = int(hashlib.md5(link.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.app{numeric_id}"
    updated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    size_bytes = 100 * 1024 * 1024
    size_str = "100.0 MB"

    app_entry = {
        "id": numeric_id,
        "name": name,
        "version": "1.0",
        "size": size_str,
        "icon": "https://ashtemobile.site/logo.png",
        "badge": "",
        "type": "games",
        "install_url": link,
        "download_url": link,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile",
        "subtitle": "IPAOMTK Direct",
        "localizedDescription": "Extracted via Playwright from ipaomtk.com",
        "iconURL": "https://ashtemobile.site/logo.png",
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": "1.0",
                "date": updated_at,
                "localizedDescription": None,
                "downloadURL": link,
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
    print(f" + Added: {name}")

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

print(f"\nDone! Successfully saved {len(apps_list)} apps into {json_file}.")
print("=== FINISHED ===")
