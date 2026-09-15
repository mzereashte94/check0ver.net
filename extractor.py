import json
import re
import requests

base_url = (
    "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf&page="
)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
        "AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 "
        "Safari/604.1"
    )
}

all_apps = []

print("Starting to fetch all apps and dynamic links from CheckOver...")

# گەڕان بەناو هەموو پەڕەکاندا بۆ وەرگرتنی نوێترین داتا
for page in range(1, 161):
  url = f"{base_url}{page}"
  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      match = re.search(r'data-page="([^"]+)"', response.text)
      if match:
        html_escape_decoded = (
            match.group(1)
            .replace("&quot;", '"')
            .replace("&amp;", "&")
            .replace("&#039;", "'")
        )
        page_data = json.loads(html_escape_decoded)

        paginator = (
            page_data.get("props", {})
            .get("paginator", {})
            .get("data", [])
        )
        if not paginator:
          break

        for app in paginator:
          name = app.get("name")
          version = app.get("version")
          size = app.get("size")
          uuid = app.get("uuid")
          bundle = app.get("bundle")
          
          # لینکی ڕەسەن و کارا کە ڕاستەوخۆ دەبەسترێتەوە بە ماڵپەڕەکەوە
          app_link = f"https://check0ver.net/en/iapps/{uuid}"

          app_info = {
              "name": name,
              "version": version,
              "size": size,
              "bundle": bundle,
              "uuid": uuid,
              "link": app_link,
          }
          all_apps.append(app_info)

        print(f"Page {page} processed. Total apps: {len(all_apps)}")
    else:
      break
  except Exception as e:
    print(f"Error on page {page}: {e}")

# پاشەکەوتکردنی داتاکان لە فایلی JSON بە ناوی داواکراو
output_filename = "ashtemobile94.json"
with open(output_filename, "w", encoding="utf-8") as f:
  json.dump(all_apps, f, ensure_ascii=False, indent=4)

print(
    f"Successfully saved {len(all_apps)} apps into '{output_filename}'!"
)
