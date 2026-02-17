import requests
from bs4 import BeautifulSoup

pnu = "2671034027100080001"
# Try variant URL for building info
url = "https://www.eum.go.kr/web/ar/lu/luLandDetRelateInfo.jsp"
params = {'pnu': pnu, 'mode': 'search', 'isNoScr': 'script', 'gubun': 'build'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f"Fetching Relate Info (Build) for PNU: {pnu}")
res = requests.get(url, params=params, headers=headers)
print(f"Status: {res.status_code}")
soup = BeautifulSoup(res.text, 'html.parser')

tables = soup.find_all('table')
print(f"Found {len(tables)} tables")
for i, table in enumerate(tables):
    print(f"Table {i}: {table.find('caption').get_text(strip=True) if table.find('caption') else ''}")
    for r in table.find_all('tr')[:5]:
        print([c.get_text(strip=True) for c in r.find_all(['th', 'td'])])
