
import requests
import urllib.parse
import xml.etree.ElementTree as ET

# Key 1
key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"

def check():
    full_url = f"{url}?serviceKey={key}&numOfRows=1&pageNo=1&SIDO={urllib.parse.quote('경기도')}&CTGR_ID=10000"
    try:
        print(f"URL: {full_url}")
        r = requests.get(full_url, timeout=30)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print(r.text[:500])
            if '<item>' in r.text:
                root = ET.fromstring(r.text)
                item = root.find('.//item')
                for child in item:
                    print(f"{child.tag}: {child.text}")
    except Exception as e:
        print(f"Error: {e}")

check()
