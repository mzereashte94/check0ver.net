import requests
import re

print("=== HUNTING FOR EXACT TABLE NAME IN JS ===")
js_url = "https://tryipa.com/assets/index-Jb0mx1SV.js"

try:
    res = requests.get(js_url, timeout=15)
    text = res.text
    
    print("\n--- LOOKING FOR SUPABASE .from() CALLS ---")
    # گەڕان بەدوای کۆدی ستانداردی سوپابەیس بۆ هێنانی داتا
    from_matches = re.findall(r'\.from\(\s*["\']([^"\']+)["\']\s*\)', text)
    if from_matches:
        unique_tables = list(set(from_matches))
        print(f"Found {len(unique_tables)} table names used in the code:")
        for t in unique_tables:
            print(f" -> {t}")
    else:
        print("No .from() calls found.")
        
    print("\n--- LOOKING FOR DIRECT ENDPOINTS ---")
    # گەڕان بەدوای لینکی ڕاستەوخۆی API
    endpoint_matches = re.findall(r'/(?:rest|functions)/v1/([^"\'\?]+)', text)
    if endpoint_matches:
        unique_endpoints = list(set(endpoint_matches))
        for e in unique_endpoints:
            print(f" -> {e}")
    else:
        print("No direct endpoints found.")
        
    print("\n--- LOOKING FOR FETCH CALLS ---")
    # گەڕان بەدوای فەنکشنی fetch
    fetch_matches = re.findall(r'fetch\(\s*["\']([^"\']+)["\']', text)
    if fetch_matches:
        for f in list(set(fetch_matches)):
            if 'http' in f or 'api' in f:
                print(f" -> {f}")

except Exception as e:
    print(f"Error: {e}")

print("\n=== HUNT FINISHED ===")
