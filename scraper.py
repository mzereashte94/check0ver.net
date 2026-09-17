import requests

print("=== PROBING TRUE API (supapi.trystore.net) ===")

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.55",
    "Origin": "https://tryipa.com",
    "Referer": "https://tryipa.com/"
}

base_url = "https://supapi.trystore.net"
endpoints = [
    "/apps",
    "/api/apps",
    "/ipas",
    "/api/ipas",
    "/v1/apps",
    "/api/library",
    "/library"
]

for ep in endpoints:
    url = base_url + ep
    print(f"\nTesting: {url}")
    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f" -> Status: {res.status_code}")
        
        if res.status_code == 200:
            print(" -> SUCCESS! Found the data:")
            # پیشاندانی 300 پیتی سەرەتا بۆ ئەوەی بزانین یارییەکانن یان نا
            print(res.text[:300]) 
    except Exception as e:
        print(f" -> Error: {e}")
        
print("\n=== PROBE FINISHED ===")
