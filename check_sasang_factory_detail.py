import requests
import xml.etree.ElementTree as ET
import os
import urllib.parse
from datetime import datetime
import sys
import io

# Set UTF-8 encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load API Keys from .env
PUBLIC_DATA_KEYS = []
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if 'PUBLIC_DATA_KEY_1' in line:
                PUBLIC_DATA_KEYS.append(line.split('=')[1].strip().strip("'").strip('"'))
            if 'PUBLIC_DATA_KEY_2' in line:
                PUBLIC_DATA_KEYS.append(line.split('=')[1].strip().strip("'").strip('"'))

sigungu_cd = '26530'  # Sasang-gu
api_url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"

# Get last 24 months
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

print(f"Sasang-gu (26530) Factory/Warehouse Transactions - Last 24 months")
print("=" * 100)

all_transactions = []

for month in months:
    for api_key in PUBLIC_DATA_KEYS:
        if not api_key:
            continue
            
        enc_key = urllib.parse.quote(api_key) if '%' not in api_key else api_key
        query = f"{api_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={month}"
        
        try:
            res = requests.get(connector_url, params={'url': query}, timeout=10)
            if res.status_code == 200 and "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                
                for item in items:
                    def get_t(tag):
                        el = item.find(tag)
                        return el.text.strip() if el is not None and el.text else ''
                    
                    transaction = {
                        'date': f"{get_t('dealYear')}-{get_t('dealMonth').zfill(2)}-{get_t('dealDay').zfill(2)}",
                        'dong': get_t('umdNm'),
                        'jibun': get_t('jibun'),
                        'amount': get_t('dealAmount'),
                        'buildingUse': get_t('buildingUse'),
                        'buildYear': get_t('buildYear'),
                        'buildingAr': get_t('buildingAr'),
                        'plottageAr': get_t('plottageAr')
                    }
                    all_transactions.append(transaction)
                
                print(f"[{month}] Found {len(items)} transactions")
                break
        except Exception as e:
            pass

print("\n" + "=" * 100)
print(f"TOTAL: {len(all_transactions)} transactions found\n")

if all_transactions:
    # Sort by date descending
    all_transactions.sort(key=lambda x: x['date'], reverse=True)
    
    print(f"{'Date':<12} | {'Location':<30} | {'Amount':<12} | {'Use':<15} | {'Year':<6}")
    print("-" * 100)
    
    for t in all_transactions:
        location = f"{t['dong']} {t['jibun']}"
        print(f"{t['date']:<12} | {location:<30} | {t['amount']:<12} | {t['buildingUse']:<15} | {t['buildYear']:<6}")
