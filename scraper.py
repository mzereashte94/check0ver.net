import requests
import re

print("=== DEEP DIVING INTO THE JS FILE ===")
js_url = "https://tryipa.com/assets/index-Jb0mx1SV.js"

try:
    print(f"Downloading JS file: {js_url}")
    res = requests.get(js_url, timeout=15)
    print(f"File downloaded. Size: {len(res.text)} bytes")
    
    # دۆزینەوەی ئەو شوێنانەی کە ناوی سێرڤەرەکەی تێدا هاتووە
    api_mentions = [m.start() for m in re.finditer(r'supapi\.trystore\.net', res.text)]
    print(f"\nFound 'supapi.trystore.net' {len(api_mentions)} times in the code.")
    
    for idx, pos in enumerate(api_mentions):
        start = max(0, pos - 150)
        end = min(len(res.text), pos + 250)
        print(f"\n--- Secret Mention {idx + 1} ---")
        print(res.text[start:end])
        
    # گەڕان بەدوای وشەی نهێنی یان کلیل (API Key)
    keys = re.findall(r'["\'](eyJ[^"\']+|anon|apikey|Authorization|Bearer [^"\']+)["\']', res.text)
    if keys:
        print("\n--- POSSIBLE API KEYS FOUND ---")
        unique_keys = list(set(keys))
        for k in unique_keys[:5]:
            print(f"Key: {k[:50]}...")
            
except Exception as e:
    print(f"Error: {e}")

print("\n=== DIVE FINISHED ===")
