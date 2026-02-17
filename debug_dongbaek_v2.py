import requests
from bs4 import BeautifulSoup
import json

pnu = "2671025624103030001"
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
}
session.headers.update(headers)

# 1. Visit main page
session.get("https://www.eum.go.kr/web/am/amMain.jsp")

# 2. Extract land det
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
params = {'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}
res = session.get(url, params=params, timeout=10)

print(f"Status: {res.status_code}")
if "present_mark1" in res.text:
    print("SUCCESS: present_mark1 found in HTML")
    soup = BeautifulSoup(res.text, 'html.parser')
    z1 = soup.find(id='present_mark1')
    print(f"Content: {z1.get_text(strip=True)}")
else:
    print("FAIL: present_mark1 NOT found in HTML")
    with open('failed_land_det.html', 'w', encoding='utf-8') as f:
        f.write(res.text)
    print("Saved HTML to failed_land_det.html")
