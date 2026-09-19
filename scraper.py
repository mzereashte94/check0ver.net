import hashlib
import json
import requests
from datetime import datetime
import concurrent.futures

print("=== ASHTE MOBILE: ULTRA-FAST EXACT COPY LINK SCRAPER ===")

json_file = "ashtemobile94.json"

# کۆدەکانت وەکو خۆی پارێزراون
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

session = requests.Session()
session.headers.update(headers)

raw_apps = []

print("Step 1: Fetching all pages extremely fast...")
for page in range(1, 165):
    url = f"https://check0ver.net/en/iapps?page={page}"
    try:
        response = session.get(url, timeout=10)
        if response.status_code != 200:
            break
            
        data = response.json()
        items = data.get("props", {}).get("paginator", {}).get("data", [])
        
        if not items:
            break
            
        raw_apps.extend(items)
        if page % 20 == 0:
            print(f"  -> Scanned {page} pages, collected {len(raw_apps)} apps...")
    except Exception as e:
        break

print(f"\nStep 2: Resolving EXACT download links for {len(raw_apps)} apps using 40 threads...")

def process_app(item):
    name = item.get("name", "Unknown App")
    version = item.get("version", "1.0")
    size_str = item.get("size", "300 MB")
    icon_url = item.get("image", "https://ashtemobile.site/logo.png")
    bundle = item.get("bundle", "com.ashtemobile.app")
    uuid = item.get("uuid", "")
    
    exact_cdn_url = ""
    dl_req_url = f"https://check0ver.net/api/iapps/{uuid}/download"
    
    try:
        # ڕاکێشانی لینکی ئەسڵی بە خێرایی
        dl_res = session.get(dl_req_url, allow_redirects=False, timeout=5)
        if dl_res.status_code in [301, 302, 303, 307, 308]:
            exact_cdn_url = dl_res.headers.get('Location', '')
        elif dl_res.status_code == 200:
            exact_cdn_url = dl_res.json().get('url', '')
    except:
        pass
        
    if not exact_cdn_url or "api/check0ver" not in exact_cdn_url:
        return None
    
    numeric_id = int(hashlib.md5(uuid.encode()).hexdigest()[:8], 16) % (10**9) if uuid else int(hashlib.md5(name.encode()).hexdigest()[:8], 16) % (10**9)
    
    size_bytes = 300 * 1024 * 1024
    try:
        if "GB" in size_str:
            size_bytes = int(float(size_str.replace("GB", "").strip()) * 1024 * 1024 * 1024)
        elif "MB" in size_str:
            size_bytes = int(float(size_str.replace("MB", "").strip()) * 1024 * 1024)
    except:
        pass

    return {
        "id": numeric_id,
        "name": name,
        "version": version,
        "size": size_str,
        "icon": icon_url,
        "badge": "MOD",
        "type": "games",
        "install_url": exact_cdn_url,
        "download_url": exact_cdn_url,
        "bundleIdentifier": bundle,
        "marketplaceID": "",
        "developerName": "AshteMobile / Check0ver",
        "subtitle": "Exact Copied Link",
        "localizedDescription": f"True CDN link for {name}.",
        "iconURL": icon_url,
        "tintColor": "#04ecfc",
        "category": "games",
        "screenshots": [],
        "versions": [
            {
                "version": version,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "localizedDescription": None,
                "downloadURL": exact_cdn_url,
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

apps_list = []
# لێرەدایە نهێنییەکە! ٤٠ یاری پێکەوە لە یەک چرکەدا دەپشکنێت
with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
    results = executor.map(process_app, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

print(f"\nTotal exact links successfully extracted: {len(apps_list)}. Generating JSON file...")

source_structure = {
    "name": "Ashtemobile",
    "subtitle": "A source for all of my apps & games",
    "description": "Catalog with exact copied CDN links.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "tintColor": "#ff007f",
    "apps": apps_list,
    "news": []
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"SUCCESS! Finished writing {len(apps_list)} exact links to {json_file}.")
