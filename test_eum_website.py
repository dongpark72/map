"""
토지이음 웹사이트에서 직접 HTML을 파싱하여 건물 정보 확인
"""
import requests
from bs4 import BeautifulSoup

# 토지이음에서 PNU로 직접 조회
pnu = "2644010400107900000"  # 부산 강서구 대저1동 790 (추정)

url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
params = {
    'pnu': pnu,
    'mode': 'search',
    'isNoScr': 'script'
}

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
}
session.headers.update(headers)

print(f"토지이음 조회: PNU={pnu}")
print("="*80)

try:
    response = session.get(url, params=params, timeout=10)
    print(f"응답 상태: {response.status_code}")
    print(f"응답 길이: {len(response.text)} bytes")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 주소 확인
        addr = soup.find(id='address') or soup.find(id='addr')
        if addr:
            print(f"\n주소: {addr.get_text(strip=True)}")
        
        # 건축물 정보 섹션 찾기
        # 토지이음에서는 건축물 정보가 별도 탭이나 섹션에 있을 수 있음
        
        # 모든 테이블 확인
        tables = soup.find_all('table')
        print(f"\n발견된 테이블 수: {len(tables)}")
        
        # 건축물 관련 텍스트 검색
        building_keywords = ['건축물', '건물', '동명칭', '주용도', '연면적']
        for keyword in building_keywords:
            elements = soup.find_all(string=lambda text: text and keyword in text)
            if elements:
                print(f"\n'{keyword}' 포함 요소 수: {len(elements)}")
                for elem in elements[:3]:  # 처음 3개만
                    print(f"  - {elem.strip()[:100]}")
        
        # HTML 일부 저장
        with open('eum_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n전체 HTML을 'eum_response.html'에 저장했습니다.")
        
except Exception as e:
    print(f"오류: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("참고: 토지이음 웹사이트에서 건축물 정보는")
print("별도의 AJAX 호출이나 다른 페이지에서 로드될 수 있습니다.")
print("="*80)
