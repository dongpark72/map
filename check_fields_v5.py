
import requests
import urllib.parse
import xml.etree.ElementTree as ET

key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"

def check():
    params = {
        "serviceKey": key,
        "numOfRows": 5,
        "pageNo": 1,
        "SIDO": "서울특별시",
        "SGK": "강남구"
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            if '<item>' in r.text:
                root = ET.fromstring(r.text)
                items = root.findall('.//item')
                if items:
                    print("\nFirst item fields:")
                    for child in items[0]:
                        print(f"{child.tag}: {child.text}")
                else:
                    print("Items node found but no item.")
            else:
                print("No <item> in response.")
                print(r.text[:500])
    except Exception as e:
        print(f"Error: {e}")

check()
