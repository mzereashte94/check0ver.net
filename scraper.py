import os
import json
import re
import requests
import subprocess

GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY")
RELEASE_TAG = "ipa-files"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

print("--- STARTING QUICK TEST (ONLY 3 APPS) ---")

url = "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf&page=1"
try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Website connection status: {response.status_code}")
    
    match = re.search(r'data-page="([^"]+)"', response.text)
    if not match:
        print("ERROR: Could not find apps data on the page! Maybe blocked.")
        exit(1)

    html_escape_decoded = match.group(1).replace("&quot;", '"').replace("&amp;", "&").replace("&#039;", "'")
    page_data = json.loads(html_escape_decoded)
    raw_apps = page_data.get("props", {}).get("paginator", {}).get("data", [])
    
    print(f"Found apps on page 1. Taking ONLY the first 3 to test...")
    test_apps = raw_apps[:3]

    for app in test_apps:
        name = app.get("name", "Unknown")
        uuid = app.get("uuid")
        print(f"\n>>> Checking App: {name}")

        trigger_url = f"https://check0ver.net/en/iapps/{uuid}/download"
        api_url = f"https://check0ver.net/api/iapps/{uuid}/download"

        print("Step 1: Trying to get direct link...")
        final_link = None

        res1 = requests.get(trigger_url, headers=headers, allow_redirects=False, timeout=10)
        print(f"Trigger Status: {res1.status_code}")
        
        if "Location" in res1.headers and ".ipa" in res1.headers["Location"]:
            final_link = res1.headers["Location"]
        elif res1.status_code == 200:
            res2 = requests.get(api_url, headers=headers, allow_redirects=False, timeout=10)
            print(f"API Status: {res2.status_code}")
            if "Location" in res2.headers and ".ipa" in res2.headers["Location"]:
                final_link = res2.headers["Location"]

        if final_link:
            print(f"SUCCESS! Found IPA Link: {final_link[:50]}...")
            local_filename = f"{name.replace(' ', '_')}.ipa"
            print("Step 2: Downloading...")
            with requests.get(final_link, stream=True, timeout=20) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    # تەنها ١ مێگابایت داونلۆد دەکات بۆ تاقیکردنەوە خێراکە
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        break 
            print("Step 3: Download test passed! App is NOT blocking GitHub.")
        else:
            print(f"FAILED to find .ipa link for {name}. The website is blocking GitHub Actions.")

except Exception as e:
    print(f"FATAL ERROR: {e}")

print("\n--- TEST COMPLETE ---")
