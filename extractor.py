import json
import requests

url = "https://check0ver.net/en/iapps?filter%5BinCategories%5D%5B0%5D=9c60f563-1983-42f0-8882-a26207bd4aaf"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
        "AppleWebKit/605.1.55 (KHTML, like Gecko) Version/16.0 Mobile/15E148 "
        "Safari/604.1"
    )
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
  # لێرەدا دەتوانیت بەشێکی HTML بگەڕێیت بە دوای uuid دا
  text = response.text
  # دەتوانیت لە ڕێگەی دەقەکەوە لینکەکان دەربهێنیت
  with open("download_links.txt", "w", encoding="utf-8") as f:
    f.write(
        "لێرەدا ناوی یارییەکان و لینکەکانیان لە داتای پەڕەکەدا هەن.\n" + text
    )
  print("Done!")
