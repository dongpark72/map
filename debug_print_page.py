import requests
from bs4 import BeautifulSoup

pnu = "2671034027100080001"
url = f"https://www.eum.go.kr/web/ar/lu/luLandDetPrint.jsp?pnu={pnu}"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f"Fetching Print Page for PNU: {pnu}")
res = requests.get(url, headers=headers)
print(f"Status: {res.status_code}")
# print(res.text[:1000])

soup = BeautifulSoup(res.text, 'html.parser')
tables = soup.find_all('table')
print(f"Found {len(tables)} tables")

for i, table in enumerate(tables):
    caption = table.find('caption')
    print(f"\nTable {i}: {caption.get_text(strip=True) if caption else 'No caption'}")
    rows = table.find_all('tr')
    for r in rows[:5]:
        cells = [c.get_text(strip=True) for c in r.find_all(['th', 'td'])]
        print(f"  {cells}")
