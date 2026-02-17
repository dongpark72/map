
import requests
import urllib.parse
import xml.etree.ElementTree as ET

url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
# Key 2
key_hex = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("Testing Key 2 (HTTP)...")
try:
    params = {
        'serviceKey': key_hex,
        'pageNo': '1',
        'numOfRows': '10',
        'SIDO': '서울특별시',
        'SGK': '강남구'
    }
    r = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Body: {r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")
