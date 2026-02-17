import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
}

pnu = "1111013400101100000" # 우정국로 48
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
try:
    res = requests.get(url, params={'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}, headers=headers, timeout=10)
    print(f"Status: {res.status_code}")
    soup = BeautifulSoup(res.text, 'html.parser')

    z1 = soup.find(id='present_mark1')
    if z1:
        print(f"RAW Z1: {z1.get_text(strip=True)}")
        raw_text = z1.get_text(separator='|', strip=True)
        print(f"SEP Z1: {raw_text}")
        items1 = [it.strip() for it in raw_text.replace(',', '|').split('|') if it.strip()]
        print(f"ITEMS1: {items1}")
        
        def clean_val(v):
            v = v.split('(')[0].split('\n')[0].strip()
            m = re.search(r'.*?(지역|구역|지구|지목)', v)
            return m.group(0) if m else v
        
        if len(items1) >= 1:
            print(f"Z1-1: {clean_val(items1[0])}")
        if len(items1) >= 2:
            print(f"Z1-2: {clean_val(items1[1])}")
    else:
        print("present_mark1 not found")

    z2 = soup.find(id='present_mark2')
    if z2:
        print(f"RAW Z2: {z2.get_text(strip=True)}")
except Exception as e:
    print(f"Error: {e}")
