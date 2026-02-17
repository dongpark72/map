import requests
import xml.etree.ElementTree as ET
import os
import urllib.parse

# Get key from .env
PUBLIC_DATA_KEY = ""
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if 'PUBLIC_DATA_KEY_1' in line:
                PUBLIC_DATA_KEY = line.split('=')[1].strip().strip("'").strip('"')

def check_factory(sigungu, month):
    # Try both variants
    urls = [
        'http://apis.data.go.kr/1613000/RTMSDataSvcIndTrade/getRTMSDataSvcIndTrade',
        'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    ]
    connector = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    for url in urls:
        enc_key = urllib.parse.quote(PUBLIC_DATA_KEY)
        query = f"{url}^serviceKey={enc_key}|LAWD_CD={sigungu}|DEAL_YMD={month}"
        
        try:
            res = requests.get(connector, params={'url': query}, timeout=10)
            print(f"URL: {url}")
            print(f"Status: {res.status_code}")
            if res.status_code == 200:
                print(f"Response (first 200 chars): {res.text[:200]}")
                if "<item>" in res.text:
                    root = ET.fromstring(res.text)
                    items = root.findall('.//item')
                    print(f"SUCCESS! Found {len(items)} items.")
                    return True
                elif "<items/>" in res.text:
                    print("Empty items list.")
                else:
                    print("No items tag found.")
        except Exception as e:
            print(f"Error: {e}")
    return False

if __name__ == "__main__":
    # 사상구 (26470)
    check_factory("26470", "202411") # Try a year ago to ensure data definitely exists
