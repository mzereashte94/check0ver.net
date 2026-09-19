import hashlib
import json
import requests
from datetime import datetime
import concurrent.futures
import sys

print("=== ASHTE MOBILE: KSIGN & FEATHER (ALTSTORE v1) SCRAPER ===")

json_file = "ashtemobile94.json"

# برا گیان! تکایە کۆدە نوێیەکانت لێرەدا دابنێ
MY_COOKIE = "لێرەدا_کۆدی_Cookie_نوێ_دابنێ"
MY_XSRF_TOKEN = "لێرەدا_کۆدی_XSRF-TOKEN_نوێ_دابنێ"

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

print("Step 1: Checking Authentication & Fetching pages...")
# پشکنینی سەرەتا بۆ ئەوەی بزانین کۆدەکان کار دەکەن یان بەسەرچوون
first_page_url = "https://check0ver.net/en/iapps?page=1"
try:
    response = session.get(first_page_url, timeout=15)
    if response.status_code != 200:
        print(f"CRITICAL ERROR: Failed to access API! Status Code: {response.status_code}")
        print("برا گیان، کۆدەکانی Cookie و XSRF-TOKEN بەسەرچوون! تکایە لە مۆبایلەکەتەوە نوێیان بکەرەوە.")
        sys.exit(1) # سکرێپتەکە دەوەستێنێت بۆ ئەوەی فایلە کۆنەکە خاڵی نەبێتەوە!
        
    data = response.json()
    items = data.get("props", {}).get("paginator", {}).get("data", [])
    if not items:
        print("ERROR: Authentication successful but zero apps found.")
        sys.exit(1)
        
    raw_apps.extend(items)
except Exception as e:
    print(f"Connection Error: {e}")
    sys.exit(1)

# هێنانی پەڕەکانی تر
for page in range(2, 165):
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
    except Exception:
        break

print(f"Step 2: Resolving links for {len(raw_apps)} apps using threads...")

def process_app(item):
    name = item.get("name", "Unknown App")
    version = item.get("version", "1.0")
    size_str = item.get("size", "300 MB")
    icon_url = item.get("image", "https://ashtemobile.site/logo.png")
    uuid = item.get("uuid", "")
    
    bundle = item.get("bundle")
    if not bundle or " " in bundle:
        bundle = f"com.ashtemobile.{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
    exact_cdn_url = ""
    dl_req_url = f"https://check0ver.net/api/iapps/{uuid}/download"
    
    try:
        dl_res = session.get(dl_req_url, allow_redirects=False, timeout=5)
        if dl_res.status_code in [301, 302, 303, 307, 308]:
            exact_cdn_url = dl_res.headers.get('Location', '')
        elif dl_res.status_code == 200:
            exact_cdn_url = dl_res.json().get('url', '')
    except:
        pass
        
    if not exact_cdn_url or "api/check0ver" not in exact_cdn_url:
        return None
    
    # چارەسەری کێشەی قەبارە (دەبێت بە ژمارە بێت نەک پیت)
    size_bytes = 314572800 
    try:
        if isinstance(size_str, str):
            if "GB" in size_str:
                size_bytes = int(float(size_str.replace("GB", "").strip()) * 1024 * 1024 * 1024)
            elif "MB" in size_str:
                size_bytes = int(float(size_str.replace("MB", "").strip()) * 1024 * 1024)
    except:
        pass

    # فۆرماتی تایبەت و سەد لە سەد دروست بۆ Ksign و Feather و AltStore
    return {
        "name": name,
        "bundleIdentifier": bundle,
        "developerName": "AshteMobile / Check0ver",
        "version": version,
        "versionDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "versionDescription": "Updated automatically.",
        "downloadURL": exact_cdn_url,
        "localizedDescription": f"True CDN link for {name}.",
        "iconURL": icon_url,
        "tintColor": "#04ecfc",
        "size": size_bytes,
        "versions": [
            {
                "version": version,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "localizedDescription": "Initial release",
                "downloadURL": exact_cdn_url,
                "size": size_bytes,
                "minOSVersion": "14.0"
            }
        ]
    }

apps_list = []
with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
    results = executor.map(process_app, raw_apps)
    for res in results:
        if res:
            apps_list.append(res)

print(f"\nTotal extracted: {len(apps_list)}. Generating JSON...")

source_structure = {
    "name": "Ashtemobile",
    "identifier": "com.ashtemobile.source", 
    "subtitle": "Ksign & Feather Source",
    "description": "Catalog with exact copied CDN links.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "tintColor": "#ff007f",
    "apps": apps_list,
    "news": []
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"SUCCESS! Check {json_file}.")
