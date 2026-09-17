import requests
import re

print("=== DEEP SEARCH FOR IPAS IN CATEGORIES & PRODUCTS ===")
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
        
        base_url = "https://supapi.trystore.net/rest/v1"
        
        # 1. هێنانی هەموو پۆلێنەکان (Categories)
        cat_res = requests.get(f"{base_url}/categories?select=*", headers=headers)
        if cat_res.status_code == 200:
            categories = cat_res.json()
            print(f"\nFound {len(categories)} categories:")
            for c in categories:
                print(f" -> [{c.get('slug')}] {c.get('name')}")
        
        # 2. هێنانی هەموو بەرهەمەکان و گەڕان بەدوای فایلی IPA یان App
        prod_res = requests.get(f"{base_url}/products?select=*", headers=headers)
        if prod_res.status_code == 200:
            products = prod_res.json()
            print(f"\nScanning {len(products)} products for apps/games...")
            
            app_count = 0
            for p in products:
                name = p.get("name", "")
                desc = str(p.get("description", ""))
                slug = p.get("slug", "")
                
                # گەڕان بەدوای ئەپ یان یاری یان لینکی داونلۆد
                if "ipa" in slug.lower() or "app" in slug.lower() or "game" in slug.lower() or "ios" in desc.lower() or "download" in desc.lower():
                    app_count += 1
                    print(f"[{app_count}] {name} (Slug: {slug})")
            
            print(f"\nTotal potential apps found: {app_count}")
            
except Exception as e:
    print(f"Error: {e}")

print("\n=== SEARCH FINISHED ===")
