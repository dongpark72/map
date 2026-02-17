import requests
from bs4 import BeautifulSoup

pnu = "2671034027100080001"
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
params = {
    'pnu': pnu,
    'mode': 'search',
    'isNoScr': 'script'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, params=params, headers=headers)
print(f"Status: {response.status_code}")
# print(f"Response length: {len(response.text)}")
# print(f"Response snippet: {response.text[:500]}")
text = response.text

if "건물명" in text:
    idx = text.find("건물명")
    print(f"Context of '건물명': {text[max(0, idx-100):idx+300]}")

if "2025" in text:
    idx = text.find("2025")
    print(f"Context of '2025': {text[max(0, idx-100):idx+300]}")

soup = BeautifulSoup(text, 'html.parser')

# Find all tables
tables = soup.find_all('table')
print(f"Found {len(tables)} tables")

for i, table in enumerate(tables):
    caption = table.find('caption')
    print(f"Table {i}: {caption.get_text(strip=True) if caption else 'No caption'}")
    # Print first row to see headers
    first_row = table.find('tr')
    if first_row:
        cells = first_row.find_all(['th', 'td'])
        print(f"  Headers: {[c.get_text(strip=True) for c in cells]}")
