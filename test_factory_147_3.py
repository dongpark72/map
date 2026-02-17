import requests
import xml.etree.ElementTree as ET
import os
import urllib.parse
from datetime import datetime

# Simulating the environment
PUBLIC_DATA_KEYS = []

# Try to get keys from .env if available
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if 'PUBLIC_DATA_KEY_1' in line:
                PUBLIC_DATA_KEYS.append(line.split('=')[1].strip().strip("'").strip('"'))
            if 'PUBLIC_DATA_KEY_2' in line:
                PUBLIC_DATA_KEYS.append(line.split('=')[1].strip().strip("'").strip('"'))

def test_factory_api(pnu):
    sigungu_cd = pnu[:5]
    api_url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # Check last 6 months
    now = datetime.now()
    months = []
    curr_y, curr_m = now.year, now.month
    for i in range(6):
        m = curr_m - i
        y = curr_y
        while m <= 0:
            m += 12
            y -= 1
        months.append(f"{y}{m:02d}")
    
    print(f"Checking {len(months)} months for Sigungu: {sigungu_cd}")
    
    for month in months:
        for api_key in PUBLIC_DATA_KEYS:
            if not api_key: continue
            enc_key = urllib.parse.quote(api_key) if '%' not in api_key else api_key
            query = f"{api_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={month}"
            
            try:
                res = requests.get(connector_url, params={'url': query}, timeout=10)
                if res.status_code == 200:
                    if "<item>" in res.text:
                        root = ET.fromstring(res.text)
                        items = root.findall('.//item')
                        print(f"Month: {month}, Found {len(items)} items")
                        for item in items[:3]: # Show first 3
                            umd = item.find('umdNm').text if item.find('umdNm') is not None else 'N/A'
                            jibun = item.find('jibun').text if item.find('jibun') is not None else 'N/A'
                            print(f"  {umd} {jibun}")
                else:
                    print(f"Month: {month}, Status: {res.status_code}")
            except Exception as e:
                print(f"Error for month {month}: {e}")

if __name__ == "__main__":
    pnu = "2647010200101470003"
    test_factory_api(pnu)
