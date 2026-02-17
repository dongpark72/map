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

def test_sigungu_transactions(sigungu_cd, target_dong, target_jibun_prefix):
    api_url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # Check last 24 months
    now = datetime.now()
    months = []
    curr_y, curr_m = now.year, now.month
    for i in range(24):
        m = curr_m - i
        y = curr_y
        while m <= 0:
            m += 12
            y -= 1
        months.append(f"{y}{m:02d}")
    
    print(f"Checking {len(months)} months for Sigungu: {sigungu_cd}")
    
    found_any = False
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
                        for item in items:
                            def get_t(it, tag):
                                el = it.find(tag); return el.text.strip() if el is not None and el.text else ''
                            
                            jibun = get_t(item, '지번') or get_t(item, 'jibun')
                            umd = get_t(item, '법정동') or get_t(item, 'umdNm')
                            
                            if target_dong in umd and target_jibun_prefix in jibun:
                                print(f"Month: {month} - MATCH: {umd} {jibun}")
                                for child in item:
                                    print(f"  {child.tag}: {child.text}")
                                found_any = True
                # else:
                #     print(f"Month: {month}, Status: {res.status_code}")
            except Exception as e:
                print(f"Error for month {month}: {e}")
                
    if not found_any:
        print(f"No transactions found for {target_jibun_prefix} in {target_dong} in the last 24 months.")

if __name__ == "__main__":
    # 부산 사상구 감전동 (26470)
    test_sigungu_transactions("26470", "감전동", "417")
