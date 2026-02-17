
import requests
import urllib.parse

# New URL from user image
URL = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

headers = {
    'User-Agent': 'Mozilla/5.0'
}

print(f"Testing URL: {URL}")

try:
    # Test 1: Standard Params
    params = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '10',
        'SIDO': '서울특별시',
        'SGK': '강남구'
    }
    r = requests.get(URL, params=params, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Body: {r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")
