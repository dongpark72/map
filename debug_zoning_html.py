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
        print("--- Z1 HTML ---")
        print(z1.prettify())
        print("--- END Z1 HTML ---")
    else:
        print("present_mark1 not found")

except Exception as e:
    print(f"Error: {e}")
