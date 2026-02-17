import requests
import xml.etree.ElementTree as ET
import urllib.parse
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gundammap.settings')
django.setup()
from maps.views import PUBLIC_DATA_KEYS

def test_apt_price():
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    # Try both http and https, and both standard and Dev
    urls = [
        "https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade",
        "http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade",
        "http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
    ]
    sigungu_cd = "11740" # 강동구
    ym = "202407"
    
    for base_url in urls:
        print(f"\n--- Testing URL: {base_url} ---")
        for api_key in PUBLIC_DATA_KEYS[:1]: # Testing one key first
            enc_key = urllib.parse.quote(api_key)
            query = f"{base_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={ym}|numOfRows=999"
            
            try:
                res = requests.get(connector_url, params={'url': query}, timeout=10)
                print(f"Status: {res.status_code}")
                print(f"Content-Type: {res.headers.get('Content-Type')}")
                print(f"Sample Text: {res.text[:500]}")
                
                if '<item>' in res.text:
                    print("SUCCESS: Found items!")
                    root = ET.fromstring(res.text)
                    items = root.findall('.//item')
                    print(f"Total items found: {len(items)}")
                    for item in items[:3]:
                        umd = item.find('umdNm').text if item.find('umdNm') is not None else 'N/A'
                        apt = item.find('aptNm').text if item.find('aptNm') is not None else 'N/A'
                        jibun = item.find('jibun').text if item.find('jibun') is not None else 'N/A'
                        print(f"  - {umd} {apt} ({jibun})")
                else:
                    print("FAILURE: No <item> tag found.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    test_apt_price()
