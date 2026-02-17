import requests
import xml.etree.ElementTree as ET
import os
import urllib.parse

PUBLIC_DATA_KEYS = []
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if 'PUBLIC_DATA_KEY_1' in line:
                PUBLIC_DATA_KEYS.append(line.split('=')[1].strip().strip("'").strip('"'))

def test_api_raw_xml(sigungu_cd, month):
    api_url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    for api_key in PUBLIC_DATA_KEYS:
        enc_key = urllib.parse.quote(api_key) if '%' not in api_key else api_key
        query = f"{api_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={month}"
        
        try:
            res = requests.get(connector_url, params={'url': query}, timeout=10)
            print(f"Month: {month}, Status: {res.status_code}")
            if res.status_code == 200:
                print(f"Response snippet: {res.text[:500]}")
                if "<item>" in res.text:
                    root = ET.fromstring(res.text)
                    items = root.findall('.//item')
                    if items:
                        print(f"First item XML:\n{ET.tostring(items[0], encoding='unicode')}")
                        return
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_api_raw_xml("26470", "202411")
