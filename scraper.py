import cloudscraper
import re

print("=== HUNTING FOR HIDDEN API ===")
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'ios', 'mobile': True})
url = "https://tryipa.com/ipa-library"

try:
    res = scraper.get(url, timeout=15)
    
    print("\n--- CHECKING BOTTOM OF HTML FOR HIDDEN DATA ---")
    print(res.text[-1000:])
    print("-----------------------------------------------\n")
    
    print("--- HUNTING INSIDE JS FILES ---")
    # دۆزینەوەی هەموو فایلە JS ەکانی سایتەکە
    js_files = re.findall(r'src=["\']([^"\']+\.js)["\']', res.text)
    
    if not js_files:
        print("No JS files found in the HTML!")
    
    for js in js_files:
        if js.startswith('/'):
            js_url = "https://tryipa.com" + js
        elif not js.startswith('http'):
            js_url = "https://tryipa.com/" + js
        else:
            js_url = js
            
        print(f"\nScanning: {js_url}")
        try:
            js_res = scraper.get(js_url, timeout=10)
            
            # گەڕان بەدوای وشەی api یان json لەناو کۆدەکاندا
            apis = re.findall(r'https://[^"\']*api[^"\']*|/api/[a-zA-Z0-9_/-]+|\.json', js_res.text)
            
            if apis:
                # سڕینەوەی ئەوانەی دووبارەن بۆ ئەوەی لیستەکە کورت بێت
                unique_apis = list(set(apis))
                print(f"Found {len(unique_apis)} possible API endpoints:")
                for api in unique_apis[:15]:  # نیشاندانی زۆرترین ١٥ دانە
                    print(f" -> {api}")
            else:
                print(" No API links found in this file.")
                
        except Exception as e:
            print(f" Failed to scan this JS file: {e}")

except Exception as e:
    print(f"Error fetching main page: {e}")
    
print("\n=== HUNT FINISHED ===")
