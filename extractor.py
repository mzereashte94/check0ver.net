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

print("Starting to fetch all pages and apps...")

# ماڵپەڕەکە نزیکەی 160 پەڕەی هەیە، دەتوانیت مەوداکە دیاری بکەیت
for page in range(1, 161):
  url = f"{base_url}{page}"
  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      # دۆزینەوەی داتای JSON لە ناو تگی data-pageـی HTMLـدا
      match = re.search(r'data-page="([^"]+)"', response.text)
      if match:
        html_escape_decoded = (
            match.group(1)
            .replace("&quot;", '"')
            .replace("&amp;", "&")
            .replace("&#039;", "'")
        )
        page_data = json.loads(html_escape_decoded)

        # وەرگرتنی لیستی یارییەکان لە paginator data
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
          download_page = f"https://check0ver.net/en/iapps/{uuid}"

          app_info = {
              "name": name,
              "version": version,
              "size": size,
              "link": download_page,
          }
          all_apps.append(app_info)

        print(f"Page {page} fetched successfully. Total apps so far: {len(all_apps)}")
    else:
      print(f"Failed to fetch page {page}, status code: {response.status_code}")
  except Exception as e:
    print(f"Error on page {page}: {e}")

# پاشەکەوتکردنی هەموو یارییەکان لە فایلێکی تێکستدا
with open("download_links.txt", "w", encoding="utf-8") as f:
  for app in all_apps:
    f.write(
        f"Name: {app['name']} | Version: {app['version']} | Size:"
        f" {app['size']}\nLink: {app['link']}\n"
        "--------------------------------------------------\n"
    )

print(
    f"Successfully extracted {len(all_apps)} apps and saved to"
    " download_links.txt!"
)
