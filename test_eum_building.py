import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# 부산광역시 강서구 대저1동 790
# 토지이음에서 직접 건축물 정보 페이지 확인
pnu = "2644011500107900000"

print(f"Checking eum.go.kr for PNU: {pnu}")
print("=" * 80)

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
}
session.headers.update(headers)

# 토지이음의 건축물 정보 페이지 확인
try:
    # 건축물 정보 페이지
    url = "https://www.eum.go.kr/web/ar/lu/luBldgList.jsp"
    params = {
        'pnu': pnu,
        'mode': 'search'
    }
    
    print(f"\nFetching: {url}")
    print(f"Params: {params}")
    
    res = session.get(url, params=params, timeout=10)
    print(f"Status: {res.status_code}")
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 테이블에서 건축물 목록 찾기
        tables = soup.find_all('table')
        print(f"\nFound {len(tables)} tables")
        
        for idx, table in enumerate(tables):
            print(f"\n--- Table {idx + 1} ---")
            rows = table.find_all('tr')
            print(f"Rows: {len(rows)}")
            
            for row_idx, row in enumerate(rows[:10]):  # 처음 10개만
                cells = row.find_all(['th', 'td'])
                if cells:
                    cell_text = [cell.get_text(strip=True) for cell in cells]
                    print(f"Row {row_idx}: {cell_text}")
        
        # 링크 찾기
        links = soup.find_all('a', href=True)
        building_links = [link for link in links if 'bldg' in link['href'].lower() or '동' in link.get_text()]
        
        print(f"\n\nBuilding-related links found: {len(building_links)}")
        for link in building_links[:5]:
            print(f"- {link.get_text(strip=True)}: {link['href']}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# 다른 API 시도 - 건축물대장 전체 조회
print("\n" + "=" * 80)
print("Trying getBrExposPubuseAreaInfo API (전유공용면적)")
print("=" * 80)

try:
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrExposPubuseAreaInfo"
    api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    
    sigungu = pnu[0:5]
    bjdong = pnu[5:10]
    platGb = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15]))
    ji = str(int(pnu[15:19]))
    
    q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=100"
    
    res = session.get(connector_url, params={'url': q}, timeout=10)
    
    if res.status_code == 200 and '<response>' in res.text:
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        print(f"Found {len(items)} items")
        
        if items:
            for idx, item in enumerate(items[:3], 1):
                print(f"\n--- Item {idx} ---")
                for child in item:
                    if child.text and child.text.strip():
                        print(f"{child.tag}: {child.text}")
        else:
            result_code = root.find('.//resultCode')
            result_msg = root.find('.//resultMsg')
            print(f"Result Code: {result_code.text if result_code is not None else 'N/A'}")
            print(f"Result Message: {result_msg.text if result_msg is not None else 'N/A'}")
            
except Exception as e:
    print(f"Error: {e}")
