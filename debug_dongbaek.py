import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re as pyre
import json

pnu = "2671025624103030001"
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
}
session.headers.update(headers)

structured_data = {
    'land': {
        '소재지': '', '용도지역1': '', '용도지역2': '',
        '지목': '', '이용상황': '', '면적': '',
        '도로': '', '형상': '', '지세': '',
        '2025': '', '2024': '', '2023': '', '2022': ''
    },
    'building': {}
}

def fetch_land_det():
    url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
    res = session.get(url, params={'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}, timeout=10)
    print(f"Land Det Status: {res.status_code}")
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        z1 = soup.find(id='present_mark1')
        if z1:
            print(f"Found present_mark1: '{z1.get_text()}'")
            raw_text = z1.get_text(separator='|', strip=True)
            print(f"Raw text (separator=|): '{raw_text}'")
            items = [it.strip() for it in raw_text.replace(',', '|').split('|') if it.strip()]
            print(f"Items: {items}")
            
            def clean_val(v):
                v = v.split('(')[0].split('\n')[0].strip()
                m = pyre.search(r'.*?(지역|구역|지구|지목)', v)
                return m.group(0) if m else v

            if len(items) >= 1:
                structured_data['land']['용도지역1'] = clean_val(items[0])
            if len(items) >= 2:
                structured_data['land']['용도지역2'] = clean_val(items[1])

fetch_land_det()
print("\n--- Result ---")
print(json.dumps(structured_data['land'], indent=2, ensure_ascii=False))
