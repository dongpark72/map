
import requests
import urllib.parse
import xml.etree.ElementTree as ET

# Try raw key
key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"

def check():
    params = {
        "serviceKey": key,
        "numOfRows": 2,
        "pageNo": 1,
        "SIDO": "경기도",
        "CTGR_ID": "10000"
    }
    try:
        # data.go.kr sometimes needs the key to be passed as is in the params dict if using requests
        # but often it's already encoded and requests encodes it again causing issues.
        # Let's try requests with the key.
        r = requests.get(url, params=params, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Response Sample:")
            print(r.text[:1000])
            if '<item>' in r.text:
                root = ET.fromstring(r.text)
                items = root.findall('.//item')
                if items:
                    print("\nFirst item tags:")
                    for child in items[0]:
                        print(f"{child.tag}: {child.text}")
    except Exception as e:
        print(f"Error: {e}")

check()
