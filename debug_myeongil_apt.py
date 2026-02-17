import requests
import xml.etree.ElementTree as ET
import urllib.parse

# 강동구 명일동 56 (고덕현대)
# sigunguCd: 11740 (강동구)
# bjdongNm: 명일동

API_KEYS = [
    "V66G/reR80o1sA4l+8rly87gU4G82I7v1Gsm9wY/gS87yqA0rS8uHwS3nUoXv5p8e7Zg==", # Example key placeholder
    # I should use the keys from the actual environment if possible, but for a standalone test I'll try to find them.
]

# Let's try to fetch the keys from .env or just use the logic from views.py
# Actually, I can just use the connector logic if it works from here.

def test_apt_price():
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    # User's suggested URL
    base_url = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"
    sigungu_cd = "11740"
    ym = "202407"
    
    # Let's try to get the real keys from the system
    from django.conf import settings
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gundammap.settings')
    django.setup()
    from maps.views import PUBLIC_DATA_KEYS
    
    for api_key in PUBLIC_DATA_KEYS:
        enc_key = urllib.parse.quote(api_key)
        query = f"{base_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={ym}|numOfRows=999"
        
        print(f"Testing with key starting with {api_key[:10]}...")
        try:
            res = requests.get(connector_url, params={'url': query}, timeout=10)
            print(f"Status: {res.status_code}")
            if '<item>' in res.text:
                print("Found items!")
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                for item in items[:5]:
                    umd = item.find('umdNm').text if item.find('umdNm') is not None else 'N/A'
                    apt = item.find('aptNm').text if item.find('aptNm') is not None else 'N/A'
                    print(f"  - {umd} {apt}")
                return
            else:
                print("No items found in response.")
                print(res.text[:200])
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_apt_price()
