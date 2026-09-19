import hashlib
import json
import requests
import re
from datetime import datetime

print("=== ASHTE MOBILE: CHECK0VER TRUE CDN LINK RESOLVER ===")

json_file = "ashtemobile94.json"

# ئەمە هەمان کۆدی نهێنی خۆتە کە پێشتر داماننا
MY_COOKIE = "XSRF-TOKEN=eyJpdil6IlJzcllVdWRRSWHVvR2pLMEFoVUh6Q1E9PSIsInZhbHVlIjoiY3JzcE9pUDhNZFNvZ2k2MUM1UmN6MFVqdlpvazhqZ2tRNWd6emhpdnRZWXRIWUpGSmtLcGZrdEpyRWI2c3BHUVhuSW1selU3Z0Jxd1JpbG9uK29BR3VSMDhTNMllc3d0LzNiYjhiNzhQdFV1Nm5Rb2RwTjVIbTl1MzdPU0RGRjYiLCJtYWMiOiIwMDcyYmQyNWRkOTM2YzlxMTZmODZjMWUxMzg5YjZkNDFlMDNhOWRkYzRkYzk2NjBiZjl2NTMxZjIyOWEzMTU5IiwidGFnIjoiIn0%3D; checkover_session=eyJpdil6InpzWUZNR1R5V0x4ZVdKV0FiMm1TYUE9PSIsInZhbHVlIjoiaV9GTGlzb2NMSFRobnZidXlyamhUSDYreERhRE9URzRreFBXS2VzeHNkNjcrRkdESjFRNnJrVFJzVVVva05CRjZCV3JuV28raEJVVFA3SW9qZFhoWndZZzBBM20vN1Zrejg3V1g4Vm5KaExVOC9MS1d4V2JqV0ZaY1Vsdy9CZVQiLCJtYWMiOiJIOWM4ZGUzYTNmZGNjODc3OTU4NzMxM2JkZTg3YThiMDU2YmRhZmU5YmE0M2JjZTJjODUyNWE4N2E4MzJmZjU5IiwidGFnIjoiIn0%3D; remember_customer_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdil6IlloOUhhnUnBUY01wamhFeFpPTUJJb1E9PSIsInZhbHVlIjoiaVZGJUUR4c0t4YTN4dkYwVjVzUmN3czQwMHZEcHNNQ3BhMll1bncrRE5jbEVIZWx5S09RTGRERWFMeWNZSU96VGdsQWQydEZMZHhYVjNPUXNXVHh1N2tqNnU1MHQ1cVhnamlOVUdxV2npoemsxNnZpUVE1L1VRd0pSZFIYV29pSzQxcVltVktkaWRBSXdYMjNDWVkzZjZkWXhQOHE0QjlSdkt6Y00vTHprVW1wQdlo4WVE1VUVOeE5HSmVSMlZGeVp6WUxMQnlhM0JXZUhoeVF4cGtjM3BpTW5GNmRYVnpxWEF3VjBwNGIzTjZPVWx4U3l0andYUlRhWGxrUjBKU01XOWhjRWRETUcxR1duRmViVFJzY2poVmJrbGFjV0pSWVZoa2RFRklXRVZKTUVzMmFFbFVUMUU5UFNJc0ltMXlZbTZsamN3WkdFME1XRTBaV1EyTW1SbU1US3hlVEVaWkdWa1pEUTFZelUwTldJMFRaSmxPRFk1TmpaaVpUTXdZV1ZrTkRFd016TXpZamxqT1dKbVptTTRNR1FpTENKMFlXY2lPaWxpZlElM0QlM0Q="
MY_XSRF_TOKEN = "eyJpdil6IlJzcllVdWRRSWHVvR2pLMEFoVUh6Q1E9PSIsInZhbHVlIjoiY3JzcE9pUDhNZFNvZ2k2MUM1UmN6MFVqdlpvazhqZ2tRNWd6emhpdnRZWXRIWUpGSmtLcGZrdEpyRWI2c3BHUVhuSW1selU3Z0Jxd1JpbG9uK29BR3VSMDhTNMllc3d0LzNiYjhiNzhQdFV1Nm5Rb2RwTjVIbTl1MzdPU0RGRjYiLCJtYWMiOiIwMDcyYmQyNWRkOTM2YzlxMTZmODZjMWUxMzg5YjZkNDFlMDNhOWRkYzRkYzk2NjBiZjl2NTMxZjIyOWEzMTU5IiwidGFnIjoiIn0="

headers = {
    "Host": "check0ver.net",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.6.1 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/plain, */*",
    "X-Inertia": "true",
    "X-Inertia-Version": "mimusoft-ipa-check0ver-customer-1.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": MY_COOKIE,
    "X-XSRF-TOKEN": MY_XSRF_TOKEN
}

# بەکارهێنانی Session بۆ ئەوەی خێراتر بێت
session = requests.Session()
session.headers.update(headers)

apps_list = []

print("Fetching Check0ver API and extracting real CDN download links...")

for page in range(1, 15): # بۆ ئەوەی خێرا بێت و بلۆک نەبیت، با سەرەتا ١٥ پەڕە بهێنین
    url = f"https://check0ver.net/en/iapps?page={page}"
    try:
        response = session.get(url, timeout=20)
        
        if response.status_code != 200:
            print(f"Failed at page {page}. Code: {response.status_code}")
            break
            
        data = response.json()
        items = data.get("props", {}).get("paginator", {}).get("data", [])
        
        if not items:
            break
            
        for item in items:
            name = item.get("name", "Unknown App")
            version = item.get("version", "1.0")
            size_str = item.get("size", "300 MB")
            icon_url = item.get("image", "https://ashtemobile.site/logo.png")
            bundle = item.get("bundle", "com.ashtemobile.app")
            uuid = item.get("uuid", "")
            
            clean_name = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
            
            # هەنگاوی گرنگ: دۆزینەوەی لینکی ڕاستەقینەی بێ پاسۆرد
            api_dl_url = f"https://check0ver.net/api/iapps/{uuid}/download"
            real_download_url = api_dl_url
            
            try:
                # ناردنی داواکارییەک بەبێ Redirect بۆ گرتنی لینکی CDN
                dl_res = session.get(api_dl_url, allow_redirects=False, timeout=5)
                if dl_res.status_code in [301, 302, 303, 307, 308]:
                    real_download_url = dl_res.headers.get('Location', api_dl_url)
                elif dl_res.status_code == 200:
                    real_download_url = dl_res.json().get('url', api_dl_url)
            except:
                pass
                
            # دڵنیابوون لەوەی بە .ipa کۆتایی دێت بۆ ناو Esign
            if ".ipa" not in real_download_url:
                separator = "&" if "?" in real_download_url else "?"
                real_download_url += f"{separator}file={clean_name}.ipa"
            
            numeric_id = int(hashlib.md5(uuid.encode()).hexdigest()[:8], 16) % (10**9) if uuid else int(hashlib.md5(name.encode()).hexdigest()[:8], 16) % (10**9)
            
            size_bytes = 300 * 1024 * 1024
            try:
                if "GB" in size_str:
                    size_bytes = int(float(size_str.replace("GB", "").strip()) * 1024 * 1024 * 1024)
                elif "MB" in size_str:
                    size_bytes = int(float(size_str.replace("MB", "").strip()) * 1024 * 1024)
            except:
                pass

            app_entry = {
                "id": numeric_id,
                "name": name,
                "version": version,
                "size": size_str,
                "icon": icon_url,
                "badge": "MOD",
                "type": "games",
                "install_url": real_download_url,
                "download_url": real_download_url,
                "bundleIdentifier": bundle,
                "marketplaceID": "",
                "developerName": "AshteMobile",
                "subtitle": "Check0ver Verified Link",
                "localizedDescription": f"Direct CDN download link extracted for {name}.",
                "iconURL": icon_url,
                "tintColor": "#04ecfc",
                "category": "games",
                "screenshots": [],
                "versions": [
                    {
                        "version": version,
                        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                        "localizedDescription": None,
                        "downloadURL": real_download_url,
                        "size": size_bytes,
                        "buildVersion": "1.0",
                        "minOSVersion": "14.0",
                    }
                ],
                "appPermissions": {
                    "entitlements": [],
                    "privacy": {}
                },
                "patreon": [],
            }
            apps_list.append(app_entry)
            
        print(f" + Processed page {page}. Collected: {len(apps_list)} real links.")
        
    except Exception as e:
        print(f"Error on page {page}: {e}")
        break

print(f"\nExtracted {len(apps_list)} real CDN links. Generating JSON...")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Apps with direct CDN links.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "tintColor": "#ff007f",
    "apps": apps_list,
    "news": []
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"SUCCESS! Check {json_file}.")
