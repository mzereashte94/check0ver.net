import cloudscraper
import re

print("=== STARTING TRYIPA HTML TEST ===")
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'ios', 'mobile': True})
url = "https://tryipa.com/ipa-library"

try:
    print(f"Fetching {url} ...")
    res = scraper.get(url, timeout=15)
    print(f"Status Code: {res.status_code}")
    
    print("\n--- FIRST 1500 CHARACTERS OF THE PAGE ---")
    print(res.text[:1500])
    print("-----------------------------------------\n")
    
    # گەڕان بەدوای لینکی ڕاستەوخۆی .ipa لەناو کۆدەکانی سایتەکە
    ipa_links = re.findall(r'href=[\'"]?([^\'" >]+.ipa)', res.text)
    if ipa_links:
        print(f"Found {len(ipa_links)} direct .ipa links in HTML!")
        for link in ipa_links[:5]:
            print(f"Link: {link}")
    else:
        print("No direct '.ipa' links found in the HTML. They might be hidden in API.")
        
    # گەڕان بەدوای هەموو لینکەکانی تری ناو سایتەکە بۆ ئەوەی بزانین چۆن کار دەکات
    all_links = re.findall(r'href=[\'"]?([^\'" >]+)', res.text)
    print(f"Found {len(all_links)} total links on the page.")
    
except Exception as e:
    print(f"Error: {e}")
    
print("=== TEST FINISHED ===")
