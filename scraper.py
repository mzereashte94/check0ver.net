import hashlib
import json
import re
import requests
from datetime import datetime

print("=== ASHTE MOBILE: IPAOMTK DIRECT FILE EXTRACTOR ===")

# پێگەی سەرەکی سایتەکە بۆ هێنانی یاری و ئەپەکان
target_site = "https://ipaomtk.com"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

print("1. Fetching main page from ipaomtk.com...")
apps_list = []
seen_urls = set()

try:
    response = requests.get(target_site, headers=headers, timeout=15)
    if response.status_code == 200:
        html_content = response.text
        
        # گەڕان بەدوای هەموو لینکەکان کە لە file.ipaomtk.com دەست پێدەکەن و بە .ipa کۆتایی دێن
        ipa_links = list(set(re.findall(r'(https?://file\.ipaomtk\.com/[^\s\'"<>]+?\.ipa)', html_content, re.IGNORECASE)))
        
        # ئەگەر لەناو جاڤاسکریپت یان سکرپتەکاندا شاردبێتیانەوە، ئەوانیش دەگەڕێین
        js_files = re.findall(r'src=["\']([^"\']+\.js)["\']', html_content)
        for js in js_files:
            js_url = js if js.startswith('http') else f"{target_site}{js if js.startswith('/') else '/' + js}"
            try:
                js_res = requests.get(js_url, headers=headers, timeout=10)
                more_links = re.findall(r'(https?://file\.ipaomtk\.com/[^\s\'"<>]+?\.ipa)', js_res.text, re.IGNORECASE)
                ipa_links.extend(more_links)
            except:
                pass

        ipa_links = list(set(ipa_links))
        print(f"Found {len(ipa_links)} direct file links! Formatting into JSON...")

        for link in ipa_links:
            if link in seen_urls:
                continue
            seen_urls.add(link)

            # دروستکردنی ناوی یارییەکە لەسەر بنەمای لینکەکەی
            parts = link.split('/')
            raw_name = parts[-2] if len(parts) >= 2 else "App"
            name = raw_name.replace('-', ' ').replace('_', ' ').title()
            
            numeric_id = int(hashlib.md5(link.encode()).hexdigest()[:8], 16) % (10**9)
            bundle = f"com.ashtemobile.app{numeric_id}"
            updated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
            
            # بەدەستهێنانی قەبارەی فایلەکە بە شێوەیەک کە سێرڤەرەکە قورس نەبێت
            size_bytes = 100 * 1024 * 1024
            size_str = "100.0 MB"
            try:
                head_res = requests.head(link, headers=headers, timeout=5)
                if 'Content-Length' in head_res.headers:
                    size_bytes = int(head_res.headers['Content-Length'])
                    size_str = f"{round(size_bytes / (1024 * 1024), 2)} MB"
            except:
                pass

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
                "localizedDescription": "Direct download link extracted from IPAOMTK.",
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

except Exception as e:
    print(f"Error fetching site: {e}")

# فۆرماتی کۆتایی فایلی JSON
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

print(f"\nDone! Successfully saved {len(apps_list)} direct files into {output_filename}.")
print("=== FINISHED ===")
