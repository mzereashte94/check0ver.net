import requests
import re
import json

print("=== EXTRACTING APPS FROM 'products' TABLE ===")
js_url = "https://tryipa.com/assets/index-Jb0mx1SV.js"

try:
    # هێنانەوەی کلیلە شاراوەکە
    res = requests.get(js_url, timeout=15)
    match = re.search(r'["\'](eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)["\']', res.text)
    
    if match:
        api_key = match.group(1)
        
        headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # چوونە ناو خشتەی products
        url = "https://supapi.trystore.net/rest/v1/products?select=*"
        print(f"Fetching apps from: {url}\n")
        
        r = requests.get(url, headers=headers, timeout=15)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            apps = r.json()
            print(f"-> BINGO! Successfully retrieved {len(apps)} apps (products)!\n")
            
            if len(apps) > 0:
                print("--- DATA STRUCTURE OF THE FIRST APP ---")
                # پیشاندانی زانیارییەکانی یەکەم یاری بۆ بینینی لینکەکە
                print(json.dumps(apps[0], indent=2, ensure_ascii=False))
                print("---------------------------------------")
        else:
            print(f"Failed to fetch data. Error: {r.text}")
            
    else:
        print("Could not find API key.")
        
except Exception as e:
    print(f"Error: {e}")

print("\n=== EXTRACTION FINISHED ===")
