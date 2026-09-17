import requests
import re

print("=== SCANNING ALL PRODUCTS FOR IPA FILES ==js")
js_url = "https://tryipa.com/assets/index-Jb0mx1SV.js"

try:
    res = requests.get(js_url, timeout=15)
    match = re.search(r'["\'](eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)["\']', res.text)
    
    if match:
        api_key = match.group(1)
        headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        url = "https://supapi.trystore.net/rest/v1/products?select=*"
        r = requests.get(url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            products = r.json()
            print(f"Total items in store: {len(products)}\n")
            
            ipa_count = 0
            for p in products:
                name = p.get("name", "Unknown")
                # پشکنینی ناو یان دیسکڕپشن بۆ دۆزینەوەی لینکی ipa یان فایل
                text_blob = str(p)
                if ".ipa" in text_blob or "download" in text_blob.lower() or "install" in text_blob.lower():
                    ipa_count += 1
                    print(f"[{ipa_count}] Found potential app: {name}")
                    print(f"    Slug: {p.get('slug')}")
            
            if ipa_count == 0:
                print("No direct .ipa strings found in product details. Let's check custom_fields or other tables.")
                # پیشاندانی ناوەکانی یەک دوو دانەی تر
                for i in range(min(5, len(products))):
                    print(lambda: None)
                    print(f" - {products[i].get('name')}")
        else:
            print(f"Error: {r.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== SCAN FINISHED ===")
