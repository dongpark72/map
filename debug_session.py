import requests
from bs4 import BeautifulSoup

pnu = "2671034027100080001"
# pnu = "1114010300100310000" # Seoul City Hall for test
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

# 1. Main page to get cookies
session.get("https://www.eum.go.kr/web/am/amMain.jsp", headers=headers)

# 2. Land info page
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
params = {'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}
print(f"Fetching with Session: {pnu}")
res = session.get(url, params=params, headers=headers)
print(f"Status: {res.status_code}")

if "신평리" in res.text or "회현동" in res.text:
    print("SUCCESS: Found address keywords in response!")
else:
    print("FAILURE: Keywords not found.")
    print(f"Snippet: {res.text[:500]}")

soup = BeautifulSoup(res.text, 'html.parser')
tables = soup.find_all('table')
print(f"Found {len(tables)} tables")
