import hashlib
import json
import re
import cloudscraper
import concurrent.futures
from datetime import datetime

print("=== ASHTE MOBILE: POWERFUL TRYIPA EXTRACTOR ===")

# ١. تێکشکاندنی سکویریتی سایتەکە و هێنانی داتاکان
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'ios', 'mobile': True})
url = "https://tryipa.com/ipa-library"

print("1. Fetching data from TryIPA and bypassing security...")
try:
    res = scraper.get(url, timeout=15)
    all_content = res.text
    
    # گەڕان بەدوای فایلە جاڤاسکریپتەکان نەوەک لینکیان تێدا شاردبێتەوە
    js_files = re.findall(r'src=["\']([^"\']+\.js)["\']', res.text)
    for js in js_files:
        js_url = js if js.startswith('http') else f"https://tryipa.com{js if js.startswith('/') else '/' + js}"
        try:
            js_res = scraper.get(js_url, timeout=10)
            all_content += " " + js_res.text
        except:
            pass
            
except Exception as e:
    print(f"Failed to fetch site: {e}")
    all_content = ""

# دەرهێنانی تەنها لینکە ڕاستەقینەکانی .ipa
raw_ipa_links = list(set(re.findall(r'(https?://[^\s\'"<>]+?\.ipa)', all_content)))
print(f"Found {len(raw_ipa_links)} raw .ipa links. Now extracting details really fast...")

# فەنکشنی سەرەکی بۆ ڕێکخستنی یارییەکان ڕێک وەکو کۆدەکەی خۆت
def process_ipa(link):
    # دروستکردنی ناو لە لینکەکەوە
    raw_name = link.split('/')[-1].split('.ipa')[0]
    name = raw_name.replace('-', ' ').replace('_', ' ').replace('%20', ' ').title()
    if not name:
        name = "Unknown App"
        
    numeric_id = int(hashlib.md5(link.encode()).hexdigest()[:8], 16) % (10**9)
    bundle = f"com.ashtemobile.{numeric_id}"
    updated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    # خاڵی بەهێزی سکرێپتەکە: پشکنینی قەبارەی فایلەکە بە خێرایی (HEAD request)
    size_bytes = 50 * 1024 * 1024 # دانانی 50MB وەکو یەدەگ
    size_str = "50.0 MB"
    try:
        head_res = scraper.head(link, timeout=5)
        if 'Content-Length' in head_res.headers:
            size_bytes = int(head_res.headers['Content-Length'])
            size_str = f"{round(size_bytes / (1024 * 1024), 1)} MB"
    except:
        pass

    return {
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
        "subtitle": "TryIPA Library",
        "localizedDescription": "Downloaded and processed automatically by AshteMobile Extractor.",
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

apps_list = []

# بەکارهێنانی ThreadPoolExecutor ڕێک وەکو ئەوەی داوات کردووە بۆ خێرایی شێتانە!
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(process_ipa, raw_ipa_links)
    for res in results:
        if res:
            apps_list.append(res)

# فۆرماتی کۆتایی فایلەکە بە ستانداردی سۆرسەکەت
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

output_filename = "ashtemobile94.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"\nDone! Extracted and formatted {len(apps_list)} apps with the powerful structure.")
print("=== FINISHED ===")
