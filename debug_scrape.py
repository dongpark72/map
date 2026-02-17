import requests
from bs4 import BeautifulSoup

url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
params = {'pnu': '2644010100107900000', 'mode': 'search', 'isNoScr': 'script'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

try:
    print(f"Fetching {url} with params {params}...")
    res = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"Status Code: {res.status_code}")
    
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Check land_build
    table = soup.find('table', {'id': 'land_build'})
    if table:
        print("FOUND table with id='land_build'")
        rows = table.find_all('tr')
        print(f"Row count: {len(rows)}")
        for i, row in enumerate(rows):
            # Print cell contents
            cells = [c.get_text(strip=True) for c in row.find_all(['th', 'td'])]
            print(f"Row {i}: {cells}")
    else:
        print("NOT FOUND table with id='land_build'")
        # Check other tables
        tables = soup.find_all('table')
        print(f"Total tables found: {len(tables)}")
        for i, t in enumerate(tables):
            txt = t.get_text(strip=True)
            if '건물동명' in txt or '대장종류' in txt:
                print(f"Table {i} matches keywords: {txt[:100]}...")
                
except Exception as e:
    print(f"Error: {e}")
