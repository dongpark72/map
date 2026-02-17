"""
토지이음 웹사이트에서 건축물 정보를 가져오는 방법 분석
"""
import requests
from bs4 import BeautifulSoup

pnu = "2644010400107900000"  # 부산 강서구 대저1동 790

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
}
session.headers.update(headers)

print("="*80)
print("토지이음 건축물 정보 조회 분석")
print("="*80)

# 1. 토지 상세 페이지 접근
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
params = {'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}

print(f"\n[1] 토지 상세 페이지 접근: {url}")
print(f"    PNU: {pnu}")

try:
    response = session.get(url, params=params, timeout=10)
    print(f"    응답 상태: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 주소 확인
        addr = soup.find(id='address') or soup.find(id='addr')
        if addr:
            print(f"    주소: {addr.get_text(strip=True)}")
        
        # 건축물 관련 링크나 버튼 찾기
        print(f"\n[2] 건축물 관련 요소 찾기:")
        
        # '건축물' 텍스트가 포함된 링크 찾기
        building_links = soup.find_all('a', string=lambda text: text and '건축물' in text)
        print(f"    '건축물' 링크 수: {len(building_links)}")
        for link in building_links[:3]:
            print(f"      - {link.get_text(strip=True)}: {link.get('href', 'N/A')}")
        
        # iframe 찾기 (건축물 정보가 iframe에 있을 수 있음)
        iframes = soup.find_all('iframe')
        print(f"\n    iframe 수: {len(iframes)}")
        for iframe in iframes:
            src = iframe.get('src', '')
            if src:
                print(f"      - {src}")
        
        # JavaScript에서 AJAX 호출 찾기
        scripts = soup.find_all('script')
        print(f"\n    script 태그 수: {len(scripts)}")
        
        building_ajax_urls = []
        for script in scripts:
            if script.string:
                # 건축물 관련 AJAX URL 찾기
                if '건축물' in script.string or 'building' in script.string.lower() or 'bld' in script.string.lower():
                    lines = script.string.split('\n')
                    for line in lines:
                        if 'ajax' in line.lower() or 'url' in line.lower() or '.jsp' in line:
                            print(f"      관련 코드: {line.strip()[:100]}")
                            building_ajax_urls.append(line.strip())
        
        # 건축물 정보 테이블 직접 찾기
        print(f"\n[3] 건축물 정보 테이블 찾기:")
        all_tables = soup.find_all('table')
        print(f"    전체 테이블 수: {len(all_tables)}")
        
        for idx, table in enumerate(all_tables):
            table_text = table.get_text()
            if '건축물' in table_text or '동명칭' in table_text or '주용도' in table_text:
                print(f"\n    [테이블 {idx + 1}] 건축물 관련 테이블 발견:")
                rows = table.find_all('tr')
                print(f"      행 수: {len(rows)}")
                
                for row_idx, row in enumerate(rows[:5]):  # 처음 5개 행만
                    cells = row.find_all(['th', 'td'])
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    print(f"        행 {row_idx + 1}: {cell_texts}")
        
        # HTML 일부 저장
        with open('eum_land_detail.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n    전체 HTML을 'eum_land_detail.html'에 저장했습니다.")
        
except Exception as e:
    print(f"오류: {e}")
    import traceback
    traceback.print_exc()

# 2. 건축물 정보 전용 페이지가 있는지 확인
print(f"\n{'='*80}")
print("[4] 건축물 정보 전용 페이지 시도:")
print("="*80)

# 토지이음에서 건축물 정보를 가져오는 다양한 URL 시도
building_urls = [
    "https://www.eum.go.kr/web/ar/lu/luBuildingInfo.jsp",
    "https://www.eum.go.kr/web/ar/lu/luBuildingDet.jsp",
    "https://www.eum.go.kr/web/ar/lu/luBuildingList.jsp",
    "https://www.eum.go.kr/web/ar/bd/bdBuildingDet.jsp",
]

for url in building_urls:
    print(f"\n시도: {url}")
    try:
        res = session.get(url, params={'pnu': pnu}, timeout=5)
        print(f"  응답 상태: {res.status_code}")
        if res.status_code == 200:
            if '건축물' in res.text or '동명칭' in res.text:
                print(f"  ✓ 건축물 정보 발견!")
                # HTML 저장
                filename = url.split('/')[-1].replace('.jsp', '_response.html')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(res.text)
                print(f"  HTML을 '{filename}'에 저장했습니다.")
    except Exception as e:
        print(f"  오류: {e}")

print("\n" + "="*80)
print("분석 완료. 저장된 HTML 파일을 확인하여 건축물 정보 추출 방법을 결정하세요.")
print("="*80)
