"""
Test different URL formats for eum.go.kr building detail pages
"""
import requests
from bs4 import BeautifulSoup

pk = "10311100190464"
pnu = "2620012100103180045"

# Try different URL formats
urls_to_try = [
    f"https://www.eum.go.kr/web/ar/lu/luBldgDetailPopup.jsp?mgmBldrgstPk={pk}&pnu={pnu}",
    f"https://www.eum.go.kr/web/ar/lu/luBldgDetail.jsp?mgmBldrgstPk={pk}",
    f"https://www.eum.go.kr/web/ar/lu/luBldgDetail.jsp?pnu={pnu}",
    f"https://www.eum.go.kr/web/ar/lu/luLandDet.jsp?pnu={pnu}",
]

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

for idx, url in enumerate(urls_to_try):
    print(f"\n{idx+1}. Testing: {url}")
    print("=" * 80)
    try:
        response = session.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Length: {len(response.text)} bytes")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            print(f"   Tables found: {len(tables)}")
            
            # Look for floor-related content
            if '층' in response.text or '건축물현황' in response.text:
                print("   ✓ Contains floor-related content!")
                
                # Try to find floor table
                for t_idx, table in enumerate(tables):
                    headers = [th.get_text(strip=True) for th in table.find_all('th')]
                    if '층별' in headers or '층' in headers:
                        print(f"   ✓✓ Found floor table at index {t_idx}!")
                        print(f"      Headers: {headers}")
                        rows = table.find_all('tr')[1:]
                        print(f"      Data rows: {len(rows)}")
                        if rows:
                            first_row_cells = [td.get_text(strip=True) for td in rows[0].find_all('td')]
                            print(f"      First row sample: {first_row_cells[:5]}")
    except Exception as e:
        print(f"   Error: {e}")

print("\n" + "=" * 80)
print("Test complete!")
