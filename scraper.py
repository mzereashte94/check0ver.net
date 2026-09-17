import os
import json
import re
import cloudscraper

print("=== EXTRACTING IPA LINKS FROM TRYIPA ===")

json_file = "ashtemobile94.json"

# کردنەوەی فایلی JSON یان دروستکردنی ئەگەر نەبوو
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except:
            data = {"name": "Ashte Mobile Library", "identifier": "com.ashte.store", "apps": []}
else:
    data = {"name": "Ashte Mobile Library", "identifier": "com.ashte.store", "apps": []}

# خۆدزینەوە لە سکویریتی سایتەکە
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'ios', 'mobile': True})
url = "https://tryipa.com/ipa-library"

try:
    print(f"Fetching website data from: {url} ...")
    res = scraper.get(url, timeout=15)
    all_content = res.text
    
    # هەوڵدەدەین فایلە جاڤاسکریپتەکانیش بهێنین چونکە زۆرجار لینکیان تێدا شاراوەتەوە
    js_files = re.findall(r'src=["\']([^"\']+\.js)["\']', res.text)
    for js in js_files:
        js_url = js if js.startswith('http') else f"https://tryipa.com{js if js.startswith('/') else '/' + js}"
        try:
            js_res = scraper.get(js_url, timeout=10)
            all_content += " " + js_res.text
        except:
            pass

    # دەرهێنانی هەموو لینکەکانی .ipa بە ڕێگەی Regex (ڕاوکردنی ڕاستەوخۆ)
    ipa_links = re.findall(r'(https?://[^\s\'"<>]+?\.ipa)', all_content)
            
    unique_ipas = list(set(ipa_links))
    print(f"\n-> Found {len(unique_ipas)} direct .ipa links!")

    # هێنانی ئەو لینکانەی کە پێشتر لەناو فایلەکەتدا هەن بۆ ئەوەی دووبارە نەبنەوە
    existing_urls = [app.get("downloadURL") for app in data.get("apps", [])]
    added_count = 0
    
    for link in unique_ipas:
        if link not in existing_urls:
            # دروستکردنی ناوی ئەپەکە لە لینکەکەوە (بۆ نمونە: Minecraft_1.2.ipa دەبێتە Minecraft)
            raw_name = link.split('/')[-1].split('.ipa')[0]
            app_name = raw_name.replace('-', ' ').replace('_', ' ').replace('%20', ' ').title()
            
            new_app = {
                "name": app_name,
                "version": "1.0",
                "size": "Unknown",
                "downloadURL": link,
                "install_url": link
            }
            data["apps"].append(new_app)
            added_count += 1
            print(f"+++ Added to JSON: {app_name}")
    
    # سەیڤکردنی فایلی JSON بە ڕێکوپێکی
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"\nSUCCESS! {added_count} new apps added to {json_file}.")
    
except Exception as e:
    print(f"Error: {e}")

print("=== FINISHED ===")
