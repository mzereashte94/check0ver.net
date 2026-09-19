import json
from datetime import datetime

print("=== ASHTE MOBILE: SECURE ALTSTORE SOURCE ===")

json_file = "ashtemobile94.json"

# لێرەدا دەتوانیت هەر لینکێکی ڕاستەقینەی CDN کە هەتە بینووسیت (نموونە)
apps_list = [
    {
        "name": "Check0ver App Catalog",
        "bundleIdentifier": "com.ashtemobile.catalog",
        "developerName": "AshteMobile",
        "version": "1.0",
        "versionDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "versionDescription": "Official direct links source.",
        "downloadURL": "https://check0ver.net/api/check0ver/E669C4F905734AED2E9E/166810/0de72f5207d159483e527280fc5e530f.ipa?ref=d256S2NINnZKK2pVZ1l4KzBsTndUd0NSZUd6cGVFMFYvczZOWmJJRmdZcStNWWFyTkpRYkxqRWk4UFdyRXkrbkFBL0QzeXU3Rk9sbkYvSkdKT3E3aUxVa2szcTFGTW8yVzd2YnVhdiswdGZ3QkF0cXJNVmVpekpRMnV6ZWczVDAzWUEwckhDVmhnMWpHTjVLVVV3RmFUUUx4Z0JkcFRTVzdReGZrQlR3MFUzNG0xV09LTGx4QjA5eElNaGRremhK",
        "localizedDescription": "Direct signed CDN link.",
        "iconURL": "https://ashtemobile.site/logo.png",
        "tintColor": "#04ecfc",
        "size": 314572800,
        "versions": [
            {
                "version": "1.0",
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "localizedDescription": "Initial release",
                "downloadURL": "https://check0ver.net/api/check0ver/E669C4F905734AED2E9E/166810/0de72f5207d159483e527280fc5e530f.ipa?ref=d256S2NINnZKK2pVZ1l4KzBsTndUd0NSZUd6cGVFMFYvczZOWmJJRmdZcStNWWFyTkpRYkxqRWk4UFdyRXkrbkFBL0QzeXU3Rk9sbkYvSkdKT3E3aUxVa2szcTFGTW8yVzd2YnVhdiswdGZ3QkF0cXJNVmVpekpRMnV6ZWczVDAzWUEwckhDVmhnMWpHTjVLVVV3RmFUUUx4Z0JkcFRTVzdReGZrQlR3MFUzNG0xV09LTGx4QjA5eElNaGRremhK",
                "size": 314572800,
                "minOSVersion": "14.0"
            }
        ]
    }
]

source_structure = {
    "name": "Ashtemobile",
    "identifier": "com.ashtemobile.source", 
    "subtitle": "Ksign & Feather Source",
    "description": "Secure working source.",
    "iconURL": "https://ashtemobile.site/logo.png",
    "website": "https://ashtemobile.site/",
    "tintColor": "#ff007f",
    "apps": apps_list,
    "news": []
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(source_structure, f, ensure_ascii=False, indent=4)

print(f"SUCCESS! Saved to {json_file}")
