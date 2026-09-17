import json
import urllib.request

print("=== FETCHING REAL APPS FOR ASHTE MOBILE ===")

json_file = "ashtemobile94.json"

# بەکارهێنانی سەرچاوەیەکی کراوە و فەرمی کە پڕە لە فایلی .ipa
source_url = "https://apps.altstore.io"

# ئامادەکردنی قاڵبی فایلی JSONـەکەت
data = {
    "name": "Ashte Mobile Library",
    "identifier": "com.ashtemobile94.store",
    "apps": []
}

try:
    print(f"Downloading apps from open source library: {source_url} ...")
    req = urllib.request.Request(source_url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=15).read().decode('utf-8')
    source_data = json.loads(response)
    
    fetched_apps = source_data.get("apps", [])
    print(f"Found {len(fetched_apps)} apps! Converting to your format...\n")
    
    for app in fetched_apps:
        download_url = app.get("downloadURL")
        # تەنها ئەو ئەپانە دەهێنین کە لینکی ڕاستەوخۆی .ipa یان هەیە
        if download_url and download_url.endswith(".ipa"):
            new_app = {
                "name": app.get("name", "Unknown App"),
                "version": app.get("version", "1.0"),
                "size": str(app.get("size", "Unknown")),
                "downloadURL": download_url,
                "iconURL": app.get("iconURL", ""),
                "description": app.get("localizedDescription", "No description available.")[:150] + "..."
            }
            data["apps"].append(new_app)
            print(f" + Added to JSON: {new_app['name']}")
            
except Exception as e:
    print(f"Error: {e}")
    
# سەیڤکردنی هەموو ئەپەکان لەناو فایلی ashtemobile94.json
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    
print(f"\nSUCCESS! {len(data['apps'])} real apps have been saved to {json_file}.")
print("=== FINISHED ===")
