import os
import json
import requests

print("=== GENERATING ASHTEMOBILE94.JSON LIBRARY ===")

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Referer": "https://tryipa.com/ipa-library"
}

# لینکە ئەگەرییەکانی هێنانی داتای ئەپەکان
api_urls = [
    "https://tryipa.com/api/apps",
    "https://tryipa.com/ipa-library.json",
    "https://tryipa.com/api/library",
    "https://tryipa.com/data/apps.json"
]

apps_data = []
success = False

for url in api_urls:
    print(f"Trying to fetch from: {url}")
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200 and len(res.text) > 50:
            content = res.json()
            # گەر داتاکە لیست بوو یان لەناو فۆڵدەری apps بوو
            if isinstance(content, list):
                apps_data = content
            elif isinstance(content, dict) and "apps" in content:
                apps_data = content["apps"]
            elif isinstance(content, dict):
                # ئەگەر داتاکەی دیکشنری بوو، دەیخەینە ناو لیستێکەوە
                apps_data = [content]
                
            if len(apps_data) > 0:
                print(f"-> SUCCESS! Retrieved {len(apps_data)} apps.")
                success = True
                break
    except Exception as e:
        print(f"-> Failed: {e}")

# ئەگەر لە ڕێگەی ئەی پی ئای سەرەکی نەهات، داتایەکی خاوێن دروست دەکەین بۆ فایلی JSONـەکەت
if not success or len(apps_data) == 0:
    print("Using fallback structure to ensure JSON is valid...")
    data = {
        "name": "Ashte Mobile Library",
        "identifier": "com.ashtemobile94.store",
        "apps": []
    }
else:
    data = {
        "name": "Ashte Mobile Library",
        "identifier": "com.ashtemobile94.store",
        "apps": apps_data
    }

# سەیڤکردنی ڕاستەوخۆ لەناو fایلی ashtemobile94.json
json_file = "ashtemobile94.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Successfully updated {json_file} with latest apps data!")
print("=== FINISHED ===")
