import os
import json
import re
import urllib.request

print("=== ASHTE MOBILE: CHECK0VER STYLE SCRAPER ===")

json_file = "ashtemobile94.json"

# ئامادەکردنی فایلی سەرەکی ڕێک وەکو ئەوەی داوات کردووە
data = {
    "name": "Ashte Mobile Library",
    "identifier": "com.ashtemobile94.store",
    "apps": []
}

# خۆگۆڕین بۆ وێبگەڕی ئاسایی بۆ ئەوەی سایتەکە نەزانێت ئێمە ڕۆبۆتین
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

req = urllib.request.Request('https://tryipa.com/ipa-library', headers=headers)

try:
    print("Fetching tryipa.com/ipa-library directly...")
    html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8')
    
    # ڕاکێشانی فایلە جاڤاسکریپتەکانیش نەوەک لینکەکانیان تێدا شاردبێتەوە
    js_links = re.findall(r'src=["\']([^"\']+\.js)["\']', html)
    for js in js_links:
        js_url = js if js.startswith('http') else "https://tryipa.com" + (js if js.startswith('/') else '/' + js)
        try:
            js_req = urllib.request.Request(js_url, headers=headers)
            js_content = urllib.request.urlopen(js_req, timeout=10).read().decode('utf-8')
            html += " " + js_content
        except:
            pass

    # ڕاوکردنی هەر لینکێک کە کۆتاییەکەی .ipa بێت
    ipa_links = re.findall(r'(https?://[^\s\'"<>]+?\.ipa)', html)
    unique_ipas = list(set(ipa_links))
    
    print(f"Found {len(unique_ipas)} direct IPA links.")
    
    # خستنە ناو فایلی JSONـەکەوە
    for link in unique_ipas:
        raw_name = link.split('/')[-1].split('.ipa')[0]
        app_name = raw_name.replace('-', ' ').replace('_', ' ').replace('%20', ' ').title()
        
        data["apps"].append({
            "name": app_name,
            "version": "1.0",
            "size": "Unknown",
            "downloadURL": link
        })
        print(f" + Added: {app_name}")
        
except Exception as e:
    print(f"Error while fetching: {e}")

# لێرەدا فەرمانی پێ دەکەین کە لە هەموو بارودۆخێکدا فایلەکە دروست بکات!
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    
print(f"\nSUCCESS! File '{json_file}' has been created/updated with {len(data['apps'])} apps.")
print("=== FINISHED ===")
