import requests
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
api_url = "http://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade"
sigungu_cd = "11740"
month = "202511"

params = {
    'serviceKey': api_key,
    'LAWD_CD': sigungu_cd,
    'DEAL_YMD': month,
    'numOfRows': 100,
    'pageNo': 1
}

print(f"Testing API for {month}...")
try:
    response = requests.get(api_url, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response (partial): {response.text[:500]}")
    
    if response.status_code == 200:
        if "<item>" in response.text:
            root = ET.fromstring(response.text)
            items = root.findall('.//item')
            print(f"Found {len(items)} items.")
        else:
            print("No items found or error in XML.")
except Exception as e:
    print(f"Error: {e}")
