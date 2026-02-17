import requests
import xml.etree.ElementTree as ET
import os
import urllib.parse
from datetime import datetime
import concurrent.futures

# Load API Keys from .env
PUBLIC_DATA_KEYS = []
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if 'PUBLIC_DATA_KEY_1' in line:
                PUBLIC_DATA_KEYS.append(line.split('=')[1].strip().strip("'").strip('"'))
            if 'PUBLIC_DATA_KEY_2' in line:
                PUBLIC_DATA_KEYS.append(line.split('=')[1].strip().strip("'").strip('"'))

def fetch_month(month, sigungu_cd):
    api_url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    results = []
    for api_key in PUBLIC_DATA_KEYS:
        if not api_key: continue
        enc_key = urllib.parse.quote(api_key) if '%' not in api_key else api_key
        query = f"{api_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={month}"
        
        try:
            res = requests.get(connector_url, params={'url': query}, timeout=15)
            if res.status_code == 200:
                if "<item>" in res.text:
                    root = ET.fromstring(res.text)
                    items = root.findall('.//item')
                    for item in items:
                        def get_t(tag):
                            el = item.find(tag)
                            return el.text.strip() if el is not None and el.text else ''
                        
                        data = {
                            '계약일': f"{get_t('dealYear')}-{get_t('dealMonth').zfill(2)}-{get_t('dealDay').zfill(2)}",
                            '법정동': get_t('umdNm'),
                            '지번': get_t('jibun'),
                            '건물주용도': get_t('buildingUse') or get_t('buildingUseNm'),
                            '거래금액': get_t('dealAmount'),
                            '건물면적': get_t('buildingAr'),
                            '대지면적': get_t('plottageAr'),
                            '건축년도': get_t('buildYear'),
                            '시군구': get_t('sggNm')
                        }
                        results.append(data)
                return results # Success for this month
        except Exception as e:
            pass
    return results

def main():
    sigungu_cd = "26530" # 사상구
    now = datetime.now()
    months = []
    curr_y, curr_m = now.year, now.month
    for i in range(24): # 2년
        m = curr_m - i
        y = curr_y
        while m <= 0:
            m += 12
            y -= 1
        months.append(f"{y}{m:02d}")
    
    print(f"Fetching real transaction data for Sigungu {sigungu_cd} (Sasang-gu) for the last 2 years...")
    
    all_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_month = {executor.submit(fetch_month, m, sigungu_cd): m for m in months}
        for future in concurrent.futures.as_completed(future_to_month):
            all_results.extend(future.result())
    
    # Sort by date descending
    all_results.sort(key=lambda x: x['계약일'], reverse=True)
    
    print(f"\nFound {len(all_results)} transactions for '사상구' in the last 2 years (Factory/Warehouse):")
    print("-" * 120)
    print(f"{'계약일':<11} | {'주소':<25} | {'건물주용도':<20} | {'금액(만)':>10} | {'건물(평)':>10} | {'토지(평)':>10} | {'건축년도'}")
    print("-" * 120)
    
    for r in all_results:
        addr = f"{r['법정동']} {r['지번']}"
        amount = r['거래금액'].replace(',', '')
        try:
            b_ar = float(r['건물면적']) * 0.3025
            b_pyung = f"{b_ar:.1f}"
        except: b_pyung = "-"
        
        try:
            p_ar = float(r['대지면적']) * 0.3025
            p_pyung = f"{p_ar:.1f}"
        except: p_pyung = "-"
        
        print(f"{r['계약일']:<11} | {addr:<25} | {r['건물주용도']:<20} | {amount:>10} | {b_pyung:>10} | {p_pyung:>10} | {r['건축년도']}")

if __name__ == "__main__":
    main()
