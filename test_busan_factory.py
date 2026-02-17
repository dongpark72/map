import requests
import xml.etree.ElementTree as ET
import os
import urllib.parse
from datetime import datetime

# Load API Keys from .env
PUBLIC_DATA_KEYS = []
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if 'PUBLIC_DATA_KEY_1' in line:
                PUBLIC_DATA_KEYS.append(line.split('=')[1].strip().strip("'").strip('"'))
            if 'PUBLIC_DATA_KEY_2' in line:
                PUBLIC_DATA_KEYS.append(line.split('=')[1].strip().strip("'").strip('"'))

# Test different Busan districts
test_districts = {
    '26530': 'Sasang-gu',
    '26440': 'Gangseo-gu',
    '26410': 'Nam-gu',
    '26470': 'Saha-gu',
    '26380': 'Buk-gu'
}

api_url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"

# Test recent month
test_month = '202502'

print(f"Testing Factory/Warehouse data for Busan districts ({test_month})")
print("=" * 80)

for sigungu_cd, district_name in test_districts.items():
    print(f"\n[{sigungu_cd}] {district_name}")
    
    found = False
    for api_key in PUBLIC_DATA_KEYS:
        if not api_key:
            continue
            
        enc_key = urllib.parse.quote(api_key) if '%' not in api_key else api_key
        query = f"{api_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={test_month}"
        
        try:
            res = requests.get(connector_url, params={'url': query}, timeout=10)
            if res.status_code == 200:
                if "<item>" in res.text:
                    root = ET.fromstring(res.text)
                    items = root.findall('.//item')
                    print(f"  -> Found {len(items)} transactions")
                    
                    # Show first transaction
                    if items:
                        item = items[0]
                        def get_t(tag):
                            el = item.find(tag)
                            return el.text.strip() if el is not None and el.text else ''
                        print(f"     Example: {get_t('umdNm')} {get_t('jibun')} - {get_t('dealAmount')}(10k KRW)")
                    found = True
                    break
                elif "<items/>" in res.text or "<items />" in res.text:
                    print(f"  -> No data (empty)")
                    found = True
                    break
        except Exception as e:
            pass
    
    if not found:
        print(f"  -> API call failed")

print("\n" + "=" * 80)
print("Summary: Checking if ANY Busan district has factory/warehouse transaction data")
