import hashlib
import json
import requests
from datetime import datetime

print("=== ASHTE MOBILE: CHECK0VER TRUE DIRECT CDN LINK SCRAPER ===")

json_file = "ashtemobile94.json"

# کۆدە ڕاستەقینەکانی خۆت بۆ چوونەژوورەوە
MY_COOKIE = "XSRF-TOKEN=eyJpdil6IlJzcllVdWRRSWHVvR2pLMEFoVUh6Q1E9PSIsInZhbHVlIjoiY3JzcE9pUDhNZFNvZ2k2MUM1UmN6MFVqdlpvazhqZ2tRNWd6emhpdnRZWXRIWUpGSmtLcGZrdEpyRWI2c3BHUVhuSW1selU3Z0Jxd1JpbG9uK29BR3VSMDhTNMllc3d0LzNiYjhiNzhQdFV1Nm5Rb2RwTjVIbTl1MzdPU0RGRjYiLCJtYWMiOiIwMDcyYmQyNWRkOTM2YzlxMTZmODZjMWUxMzg5YjZkNDFlMDNhOWRkYzRkYzk2NjBiZjl2NTMxZjIyOWEzMTU5IiwidGFnIjoiIn0%3D; checkover_session=eyJpdil6InpzWUZNR1R5V0x4ZVdKV0FiMm1TYUE9PSIsInZhbHVlIjoiaV9GTGlzb2NMSFRobnZidXlyamhUSDYreERhRE9URzRreFBXS2VzeHNkNjcrRkdESjFRNnJrVFJzVVVva05CRjZCV3JuV28raEJVVFA3SW9qZFhoWndZZzBBM20vN1Zrejg3V1g4Vm5KaExVOC9MS1d4V2JqV0ZaY1Vsdy9CZVQiLCJtYWMiOiJIOWM4ZGUzYTNmZGNjODc3OTU4NzMxM2JkZTg3YThiMDU2YmRhZmU5YmE0M2JjZTJjODUyNWE4N2E4MzJmZjU5IiwidGFnIjoiIn0%3D; remember_customer_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdil6IlloOUhhnUnBUY01wamhFeFpPTUJJb1E9PSIsInZhbHVlIjoiaVZGJUUR4c0t4YTN4dkYwVjVzUmN3czQwMHZEcHNNQ3BhMll1bncrRE5jbEVIZWx5S09RTGRERWFMeWNZSU96VGdsQWQydEZMZHhYVjNPUXNXVHh1N2tqNnU1MHQ1cVhnamlOVUdxV2npoemsxNnZpUVE1L1VRd0pSZFIYY29pSzQxcVltVktkaWRBSXdYMjNDWVkzZjZkWXhQOHE0QjlSdkt6Y00vTHprVW1wQdlo4WVE1VUVOeE5HSmVSMlZGeVp6WUxMQnlhM0JXZUhoeVF4cGtjM3BpTW5GNmRYVnpxWEF3VjBwNGIzTjZPVWx4U3l0andYUlRhWGxrUjBKU01XOWhjRWRETUcxR1duRmViVFJzY2poVmJrbGFjV0pSWVZoa2RFRklXRVZKTUVzMmFFbFVUMUU5UFNJc0ltMXlZbTZsamN3WkdFME1XRTBaV1EyTW1SbU1US3hlVEVaWkdWa1pEUTFZelUwTldJMFRaSmxPRFk1TmpaaVpUTXdZV1ZrTkRFd016TXpZamxqT1dKbVptTTRNR1FpTENKMFlXY2lPaWxpZlElM0QlM0Q="
MY_XSRF_TOKEN = "eyJpdil6IlJzcllVdWRRSWHVvR2pLMEFoVUh6Q1E9PSIsInZhbHVlIjoiY3JzcE9pUDhNZFNvZ2k2MUM1UmN6MFVqdlpvazhqZ2tRNWd6emhpdnRZWXRIWUpGSmtLcGZrdEpyRWI2c3BHUVhuSW1selU3Z0Jxd1JpbG9uK29BR3VSMDhTNMllc3d0LzNiYjhiNzhQdFV1Nm5Rb2RwTjVIbTl1MzdPU0RGRjYiLCJtYWMiOiIwMDcyYmQyNWRkOTM2YzlxMTZmODZjMWUxMzg5YjZkNDFlMDNhOWRkYzRkYzk2NjBiZjl2NTMxZjIyOWEzMTU5IiwidGFnIjoiIn0="

headers = {
    "Host": "check0ver.net",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.6.1 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/plain, */*",
    "X-Inertia": "true",
    "X-Inertia-Version": "mimusoft-ipa-check0ver-customer-1.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": MY_COOKIE,
    "X-XSRF-TOKEN": MY_XSRF_TOKEN,
    "Priority": "u=3, i",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

session = requests.Session()
session.headers.update(headers)

apps_list = []

print("Scanning pages and resolving TRUE DIRECT CDN links...")

for page in range(1, 165):
    url = f"https://check0ver.net/en/iapps?page={page}"
    try:
        response = session.get(url, timeout=20)
        
        if response.status_code != 200:
            print(f"Finished or stopped at page {page}.")
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
            description = item.get("description", f"Extracted from Check0ver: {name}")
            
            # هەنگاوی جادویی: داواکاری بۆ دۆزینەوەی لینکی ئەسڵی CDN بە ڕێگەی Redirect
            direct_download_url = f"https://check0ver.net/api/iapps/{uuid}/download"
            try:
                dl_res = session.get(direct_download_url, allow_redirects=False, timeout=5)
                if dl_res.status_code in [301, 302, 303, 307, 308]:
                    location = dl_res.headers.get("Location")
                    if location:
                        direct_download_url = location
                elif dl_res.status_code == 200:
                    res_json = dl_res.json()
                    if "url" in res_json:
                        direct_download_url = res_json["url"]
            except Exception as e:
                pass
            
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
                "install_url": direct_download_url,
                "download_url": direct_download_url,
                "bundleIdentifier": bundle,
                "marketplaceID": "",
                "developerName": "AshteMobile / Check0ver",
                "subtitle": "Check0ver Direct CDN Source",
                "localizedDescription": description,
                "iconURL": icon_url,
                "tintColor": "#04ecfc",
                "category": "games",
                "screenshots": [],
                "versions": [
                    {
                        "version": version,
                        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                        "localizedDescription": None,
                        "downloadURL": direct_download_url,
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
            
        print(f" + Scraped page {page}. Total true CDN links collected: {len(apps_list)}")
        
    except Exception as e:
        print(f"Error on page {page}: {e}")
        break

print(f"\nTotal collected: {len(apps_list)}. Generating JSON file...")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Welcome to my source! Catalog with true direct CDN links.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "patreonURL": "https://ashtemobile.site/Ashtemobile.json",
    "tintColor": "#ff007f",
    "featuredApps": [],
    "headerURL": "https://ashtemobile.site/logo.png",
    "apps": apps_list,
    "news": [
        {
            "title": "Instagram",
            "identifier": "news_instagram",
            "caption": "Ashtemobile",
            "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "tintColor": "#ff007f",
            "imageURL": "https://ashtemobile.site/logo.png",
            "notify": True,
            "url": "https://www.instagram.com/ashtemobile",
            "appID": None,
        }
    ]
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"SUCCESS! Finished writing {len(apps_list)} games with true direct CDN links to {json_file}.")
