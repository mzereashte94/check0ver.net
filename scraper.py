import requests
import re
import json

print("=== HUNTING FOR OTHER TABLES IN SUPABASE ===")
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
        
        # لێرەدا هەوڵ دەدین سەیری ناو ڕووی سێرڤەرەکە بکەین یان خشتە بەناوبانگەکانی تر تاقی بکەینەوە
        other_tables = ["ipas", "apps", "library", "ipa_files", "app_library", "downloads", "categories", "items", "files"]
        base_url = "https://supapi.trystore.net/rest/v1"
        
        for t in other_tables:
            url = f"{base_url}/{t}?select=*&limit=1"
            r = requests.get(url, headers=headers, timeout=10)
            print(f"Table '{t}': Status {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                print(f" >>> BINGO! Found table '{t}' with data!")
                if len(data) > 0:
                    print(json.dumps(data[0], indent=2, ensure_ascii=False))
                break
    else:
        print("API Key not found.")
except Exception as e:
    print(f"Error: {e}")

print("\n=== HUNT FINISHED ===")
