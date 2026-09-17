import json
import re
from playwright.sync_api import sync_playwright

print("=== ASHTE MOBILE: TRYIPA DEDICATED EXTRACTOR ===")

json_file = "ashtemobile94.json"

data = {
    "name": "Ashtemobile TryIPA",
    "identifier": "com.ashtemobile.tryipa",
    "apps": []
}

# لێرەدا ئەو لینکەی خۆتت داناوە، دەتوانیت هەر لینکێکی تری TryIPAـش لێرە زیاد بکەیت لە داهاتوودا
target_urls = [
    "https://tryipa.com/ipa-library/bitlife-life-simulator-mod-c031218c"
]

def run():
    with sync_playwright() as p:
        print("Launching headless browser...")
        browser = p.chromium.launch(headless=True)
        # بەکارهێنانی شێوازی مۆبایل بۆ ئەوەی سایتەکە ڕێک وەکو وێنەکەی تۆ بکرێتەوە
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            viewport={"width": 390, "height": 844}
        )
        page = context.new_page()

        for url in target_urls:
            print(f"\nNavigating directly to your link: {url}")
            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(3000) # چاوەڕێی لۆدبوونی سایتەکە دەکەین
                
                # دەرهێنانی ناوی یارییەکە
                app_name = "BitLife"
                try:
                    app_name = page.locator("h1, h2").first.inner_text()
                except:
                    pass
                
                print(f"Found App: {app_name}. Trying to extract .ipa...")

                # کرتەکردن لە دوگمەی GET بە ئۆتۆماتیکی
                print("Clicking 'GET' button...")
                page.evaluate("""
                    const buttons = Array.from(document.querySelectorAll('button, a, div'));
                    const getBtn = buttons.find(el => el.innerText && el.innerText.trim() === 'GET');
                    if (getBtn) getBtn.click();
                """)
                page.wait_for_timeout(2000) # چاوەڕێی کردنەوەی مۆدێلەکە (مەسجەکە) دەکەین
                
                # کرتەکردن لە دوگمەی Download ناو مەسجەکە
                print("Clicking 'Download' in the popup...")
                page.evaluate("""
                    const buttons = Array.from(document.querySelectorAll('button, a'));
                    const downloadBtn = buttons.find(el => el.innerText && el.innerText.includes('Download'));
                    if (downloadBtn) downloadBtn.click();
                """)
                page.wait_for_timeout(3000)

                # گەڕان بەدوای لینکی .ipa لەناو کۆدی پەڕەکەدا دوای کلیک کردنەکە
                content = page.content()
                ipa_links = list(set(re.findall(r'(https?://[^\s\'"<>]+?\.ipa)', content)))
                
                if ipa_links:
                    final_link = ipa_links[0]
                    print(f"-> BOOM! Successfully extracted IPA: {final_link}")
                    
                    data["apps"].append({
                        "name": app_name,
                        "version": "1.0",
                        "size": "Unknown",
                        "downloadURL": final_link,
                        "install_url": final_link,
                        "iconURL": "https://ashtemobile.site/logo.png"
                    })
                else:
                    print("-> Could not find .ipa link. The site might be hiding it inside an API.")
            
            except Exception as e:
                print(f"Error processing {url}: {e}")

        # سەیڤکردنی فایلی JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        browser.close()
        print("\n=== FINISHED ===")

if __name__ == "__main__":
    run()
