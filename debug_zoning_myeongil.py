import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
}

pnu = "1174010100100560000" # 강동구 명일동 56
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
try:
    res = requests.get(url, params={'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')

    z1 = soup.find(id='present_mark1')
    if z1:
        print(f"RAW Z1: {z1.get_text('|', strip=True)}")
        raw_text = z1.get_text(separator='|', strip=True)
        items1 = [it.strip() for it in raw_text.replace(',', '|').split('|') if it.strip()]
        print(f"ITEMS1: {items1}")
    else:
        print("present_mark1 not found")

except Exception as e:
    print(f"Error: {e}")
