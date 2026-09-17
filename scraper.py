import json
import os
from playwright.sync_api import sync_playwright

print("=== ASHTE MOBILE: PLAYWRIGHT NETWORK INTERCEPTOR ===")

json_file = "ashtemobile94.json"
data = {
    "name": "Ashte Mobile Library",
    "identifier": "com.ashtemobile94.store",
    "apps": []
}

found_apps = []

# ئەم فەنکشنە گوێ لە هەموو داتایەک دەگرێت کە سایتەکە دەیهێنێت
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

    # خستنەگەڕی سیخوڕەکە لەسەر هێڵی نێتۆڕک
    page.on("response", handle_response)

    print("Navigating to tryipa.com/ipa-library and waiting for JS to execute...")
    page.goto("https://tryipa.com/ipa-library", wait_until="networkidle", timeout=60000)

    # چاوەڕێکردن بۆ ماوەی 10 چرکە بۆ ئەوەی دڵنیا بین هەموو یارییەکان لە سەرچاوەکانەوە لۆد بوون
    page.wait_for_timeout(10000)
    browser.close()

if len(found_apps) > 0:
    print(f"\nProcessing {len(found_apps)} extracted apps into Ashtemobile format...")
    
    existing_urls = []
    
    for app in found_apps:
        download_url = app.get("downloadURL")
        if download_url and str(download_url).endswith(".ipa"):
            if download_url not in existing_urls:
                new_app = {
                    "name": app.get("name", "Unknown App"),
                    "version": app.get("version", "1.0"),
                    "size": str(app.get("size", "Unknown")),
                    "downloadURL": download_url,
                    "iconURL": app.get("iconURL", "https://ashtemobile.site/logo.png"),
                    "description": str(app.get("localizedDescription", "Extracted from TryIPA"))[:200]
                }
                data["apps"].append(new_app)
                existing_urls.append(download_url)
                print(f" + Added: {new_app['name']}")

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"\n=== FINISHED! Successfully extracted and saved {len(data['apps'])} real IPA links. ===")
