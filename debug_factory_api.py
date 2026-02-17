import requests
import xml.etree.ElementTree as ET
import os

# .env에서 키를 읽거나 직접 입력
service_key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
lawd_cd = '26440' # 부산 사상구
deal_ym = '202502' # 2025년 2월

# 공장 및 창고 매매 실거래가 API (HTTP로 시도)
url = 'http://apis.data.go.kr/1613000/RTMSDataSvcNIndTrade/getRTMSDataSvcNIndTrade'

params = {
    'serviceKey': service_key,
    'lawdCd': lawd_cd,
    'dealYmd': deal_ym,
}

print(f"Calling API: {url}")
print(f"Params: {params}")

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status Code: {response.status_code}")
    print("--- Raw Response (First 1000 chars) ---")
    print(response.text[:1000])
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        items = root.findall('.//item')
        print(f"\nFound {len(items)} items.")
        for i, item in enumerate(items[:3]):
            print(f"\nItem #{i+1}:")
            for child in item:
                print(f"  {child.tag}: {child.text}")
except Exception as e:
    print(f"Error: {e}")
