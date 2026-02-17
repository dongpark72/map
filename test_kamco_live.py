
import requests
import urllib.parse
import xml.etree.ElementTree as ET

KEYS = [
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368',
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
]

def test_kamco_live():
    url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
    # Use the second key which looks like a base64 key often used by data.go.kr
    key = KEYS[1]
    
    query_params = {
        "serviceKey": key,
        "numOfRows": 5,
        "pageNo": 1,
        "SIDO": "경기도",
        "SGK": "성남시",
        "CTGR_ID": "10000"
    }
    
    try:
        # requests will encode the key, but sometimes data.go.kr needs the encoded key NOT to be re-encoded.
        # Let's try direct URL construction.
        enc_key = urllib.parse.quote(key)
        full_url = f"{url}?serviceKey={enc_key}&numOfRows=5&pageNo=1&SIDO={urllib.parse.quote('경기도')}&SGK={urllib.parse.quote('성남시')}&CTGR_ID=10000"
        
        print(f"Testing URL: {full_url}")
        response = requests.get(full_url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            if '<resultCode>00</resultCode>' in response.text:
                root = ET.fromstring(response.text)
                body = root.find('body')
                if body is not None:
                    items = body.find('items')
                    if items is not None:
                        item = items.find('item')
                        if item is not None:
                            print("FIELDS FOUND:")
                            for child in item:
                                print(f"{child.tag}: {child.text}")
                            return
        print("Failed or empty response.")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")

test_kamco_live()
