import hashlib
import json
import requests
from datetime import datetime
import concurrent.futures
import sys

print("=== ASHTE MOBILE: EXACT REAL LINK ENFORCER (ALTSTORE) ===")

json_file = "ashtemobile94.json"

MY_COOKIE = "XSRF-TOKEN=eyJpdiI6IlJzcllVdWRSWHVvR2pLMEFoVUh6Q1E9PSIsInZhbHVlIjoia3JzcE9pUDhNZFNvZ2k2MUM1UmN6MFVqdlpvazhqZ2tRNWd6emhPdnRZWXRlWUpGSmtLcGFrdEpyRWI2c3BHUVhuSW1selU3Z0Jxd1JpbG9uK29BR3VSMDhTNmlIc3d0LzNiYjhiNzhQdFV1Nm5Rb2RwTjVIbTl1MzdPU0RGRjYiLCJtYWMiOiIwMDcyYmQyNWRkOTM2YzIxMTZmODZjMWUxMzg5YjZkNDFlMDNhOWRkYzRkYzk2NjBiZjI2NTMxZjIyOWEzMTU5IiwidGFnIjoiIn0%3D; checkover_session=eyJpdiI6InpzWUZNR1R5V0x4ZVdKV0FiMm1TYUE9PSIsInZhbHVlIjoiKy9GTGlsb2NMSFRobnVidXlyamhUSDYreERhRE9URzRreFBXS2VzeHNkNjcrRkdESjFRNnJrVFJzUVVva05CRjZCV3JuV28raEJVVFA3SW9qZFhoWndZZzBBM20vN1Zrejg3V1g4Vm5KaExVOC9MS1d4V2JqV0ZaY1Vsdy9CZVQiLCJtYWMiOiJlOWM4ZGUzYTNmZGNiODc3OTU4NzMxM2JkZTg3YThiMDU2YmRhZmU5YmE0M2JjZTJjODUyNWE4N2E4MzJmZjU5IiwidGFnIjoiIn0%3D; remember_customer_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ilo0UHhnUnBUY01wamhFeFpPTUJjL1E9PSIsInZhbHVlIjoiMllVZGJRUUR4c0t4YTN4dkYwVjVzUmN3czQwMHZEcHNNQ3BhMll1bncrRE5jbEVlZWx5S09RTGRERWFMeWNZSU96VGdsQWQydEZMdzhYVjNPUXNXVHh1N2tqNnU1MHQ1cVhnamlOVUdxWnpoemsxNnZpUVE1L1VQd0pSZFlYV29pSzQxcVltVktkaWRBSXdXY2NDWVkzZjZkWXhQOHE0QjlSdkt6Y00vTHprUmpQdlo4WVE1UENXNGJuR2VFYzZYL1Bya3BWeHhyQXpkc3piMnF6dXVzQXAwV0p4b3N6OUlxSytjWXRTaXlkR0JSMW9hcEdDMG1GWnFEbTRscjhVbklacWJRYVhKdEFlWEVJMEs2aElUQ1E9PSIsIm1hYyI6IjcwZGE0MWE0ZWQ2MmRmMTkxYTEzZGVkZDQ1YzU0NWI4ZDJlODY5NjZiZTMwYWVkNDEwMzMzYjljOWJmZmM4MGQiLCJ0YWciOiIifQ%3D%3D"

MY_XSRF_TOKEN = "eyJpdiI6IlJzcllVdWRSWHVvR2pLMEFoVUh6Q1E9PSIsInZhbHVlIjoia3JzcE9pUDhNZFNvZ2k2MUM1UmN6MFVqdlpvazhqZ2tRNWd6emhPdnRZWXRlWUpGSmtLcGFrdEpyRWI2c3BHUVhuSW1selU3Z0Jxd1JpbG9uK29BR3VSMDhTNmlIc3d0LzNiYjhiNzhQdFV1Nm5Rb2RwTjVIbTl1MzdPU0RGRjYiLCJtYWMiOiIwMDcyYmQyNWRkOTM2YzIxMTZmODZjMWUxMzg5YjZkNDFlMDNhOWRkYzRkYzk2NjBiZjI2NTMxZjIyOWEzMTU5IiwidGFnIjoiIn0="

headers = {
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

print("Step 1: Fetching games directly from Check0ver...")
try:
    res = session.get("https://check0ver.net/en/iapps?page=1", timeout=15)
    if res.status_code != 200:
        print("CRITICAL ERROR: Invalid Cookie or Token! The site blocked the request.")
        sys.exit(1)
    data = res.json()
    items = data.get("props", {}).get("paginator", {}).get("data", [])
    if not items:
        sys.exit(1)
    raw_apps.extend(items)
except Exception as e:
    sys.exit(1)

for page in range(2, 165):
    try:
        r = session.get(f"https://check0ver.net/en/iapps?page={page}", timeout=10)
        if r.status_code != 200:
            break
        items = r.json().get("props", {}).get("paginator", {}).get("data", [])
        if not items:
            break
        raw_apps.extend(items)
    except:
        break

def get_real_app(item):
    name = item.get("name", "Unknown App")
    version = item.get("version", "1.0")
    icon_url = item.get("image", "https://ashtemobile.site/logo.png")
    uuid = item.get("uuid", "")
    
    bundle = item.get("bundle")
    if not bundle or " " in bundle:
        bundle = f"com.ashtemobile.{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
    req_url = f"https://check0ver.net/api/iapps/{uuid}/download"
    real_link = None
    
    try:
        dl_res = session.get(req_url, allow_redirects=False, timeout=10)
        if dl_res.status_code in [301, 302, 303, 307, 308]:
            link = dl_res.headers.get('Location', '')
            if "ref=" in link or "check0ver" in link:
                real_link = link
        elif dl_res.status_code == 200:
            link = dl_res.json().get('url', '')
            if "ref=" in link or "check0ver" in link:
                real_link = link
    except:
        pass
        
    if not real_link:
        return None
        
    if ".ipa" not in real_link.split("?")[0]:
        connector = "&" if "?" in real_link else "?"
        real_link += f"{connector}file={hashlib.md5(uuid.encode()).hexdigest()}.ipa"
        
    return {
        "name": name,
        "bundleIdentifier": bundle,
        "developerName": "AshteMobile / Check0ver",
        "version": version,
        "versionDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "versionDescription": "Direct CDN Link",
        "downloadURL": real_link,
        "localizedDescription": f"Original CDN Link for {name}",
        "iconURL": icon_url,
        "tintColor": "#04ecfc",
        "size": 314572800,
        "versions": [
            {
                "version": version,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "localizedDescription": "Direct Release",
                "downloadURL": real_link,
                "size": 314572800,
                "minOSVersion": "14.0"
            }
        ]
    }

apps_list = []
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    results = executor.map(get_real_app, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

source_structure = {
    "name": "Ashtemobile",
    "identifier": "com.ashtemobile.source", 
    "subtitle": "Ksign & Feather Source",
    "description": "100% Real Direct CDN Links.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "tintColor": "#ff007f",
    "apps": apps_list,
    "news": []
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"Done! Saved to {json_file}")
