import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib.parse

# API configuration
API_KEY = 'YfL0bnXWkWTqsOkJLDNjmPyFMJvZHjXxnQVBNvDjVZdMoMQRJLSNmNdEqFJWOzSIXdBvvOoJLRGxpMQRVMVOBw=='
SIGUNGU_CD = '26530'  # Busan Sasang-gu
API_URL = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
CONNECTOR_URL = 'https://www.eum.go.kr/dataapis/UrlConnector.jsp'

# Generate last 24 months
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

print(f"Checking Factory/Warehouse Real Price Data for Sasang-gu (26530)")
print(f"Period: {months[-1]} to {months[0]}")
print("=" * 80)

total_count = 0
sample_data = []

for month in months:
    enc_key = urllib.parse.quote(API_KEY)
    query = f"{API_URL}^serviceKey={enc_key}|LAWD_CD={SIGUNGU_CD}|DEAL_YMD={month}"
    
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        res = session.get(CONNECTOR_URL, params={'url': query}, timeout=10)
        
        if res.status_code == 200:
            if "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                
                if items:
                    print(f"\n[{month}] Found {len(items)} transactions")
                    total_count += len(items)
                    
                    for idx, item in enumerate(items[:3], 1):
                        def get_t(tag):
                            el = item.find(tag)
                            return el.text.strip() if el is not None and el.text else ''
                        
                        data = {
                            'month': month,
                            'location': f"{get_t('umdNm')} {get_t('jibun')}",
                            'price': get_t('dealAmount'),
                            'type': get_t('buildingType'),
                            'use': get_t('buildingUse'),
                            'date': f"{get_t('dealYear')}-{get_t('dealMonth')}-{get_t('dealDay')}"
                        }
                        sample_data.append(data)
                        print(f"  {idx}. Location: {data['location']}")
                        print(f"     Price: {data['price']} (10k KRW)")
                        print(f"     Type: {data['type']}, Use: {data['use']}")
                        print(f"     Date: {data['date']}")
                    
                    if len(items) > 3:
                        print(f"  ... and {len(items) - 3} more")
            elif "<items/>" in res.text or "<items />" in res.text:
                pass  # No data for this month
            else:
                # Check for error messages
                if "<returnAuthMsg>" in res.text:
                    root = ET.fromstring(res.text)
                    auth_msg = root.find('.//returnAuthMsg')
                    if auth_msg is not None:
                        print(f"[{month}] API Error: {auth_msg.text}")
                else:
                    print(f"[{month}] Response preview: {res.text[:300]}")
        else:
            print(f"[{month}] HTTP Error: {res.status_code}")
            
    except Exception as e:
        print(f"[{month}] Exception: {e}")

print("\n" + "=" * 80)
print(f"TOTAL: {total_count} factory/warehouse transactions found")
print(f"\nSample data count: {len(sample_data)}")

if sample_data:
    print("\nFirst 5 samples:")
    for i, d in enumerate(sample_data[:5], 1):
        print(f"{i}. [{d['month']}] {d['location']} - {d['price']} (10k KRW)")
