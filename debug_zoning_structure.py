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
    # print(res.text[:1000])
    soup = BeautifulSoup(res.text, 'html.parser')

    # Look for any element that might contain zoning info
    # Usually it's in a table with certain classes or IDs
    for tag in soup.find_all(['td', 'div'], id=re.compile('present_mark')):
        print(f"ID: {tag.get('id')}, Content: {tag.get_text(strip=True)}")

    # Check for address to confirm we got the right page
    addr = soup.find(id='address') or soup.find(id='addr')
    print(f"Address: {addr.get_text(strip=True) if addr else 'Not found'}")

except Exception as e:
    print(f"Error: {e}")
