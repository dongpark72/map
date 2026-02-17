import requests
from bs4 import BeautifulSoup

pnu = "2671034027100080001"
# Try building info page
url = "https://www.eum.go.kr/web/ar/lu/luBuildInfo.jsp"
params = {'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f"Fetching Building Info for PNU: {pnu}")
res = requests.get(url, params=params, headers=headers)
print(f"Status: {res.status_code}")
soup = BeautifulSoup(res.text, 'html.parser')

tables = soup.find_all('table')
print(f"Found {len(tables)} tables")
for i, table in enumerate(tables):
    caption = table.find('caption')
    print(f"Table {i}: {caption.get_text(strip=True) if caption else 'No caption'}")
    # Print sample data
    rows = table.find_all('tr')[:3]
    for r in rows:
        print(f"  Row: {[c.get_text(strip=True) for c in r.find_all(['th', 'td'])]}")
