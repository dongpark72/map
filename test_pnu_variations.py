import requests
from bs4 import BeautifulSoup

# 카카오 API로 주소 검색하여 정확한 법정동 코드와 지번 확인
address = "부산광역시 강서구 대저1동 790"

# 1. 카카오 지오코더로 주소 정보 확인
kakao_key = "d4e4fc27e3e8e3e0e9e8e3e0e9e8e3e0"  # 실제 키는 settings에서
url = "https://dapi.kakao.com/v2/local/search/address.json"

print(f"검색 주소: {address}")
print("="*80)

# 네이버 부동산 또는 토지이음에서 직접 검색
# 토지이음 검색 페이지로 이동하여 PNU 확인
search_url = "https://www.eum.go.kr/web/am/amLandSearch.jsp"

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
session.headers.update(headers)

# 주소로 검색
params = {
    'addr': '부산광역시 강서구 대저1동 790'
}

try:
    response = session.get(search_url, params=params, timeout=10)
    print(f"토지이음 검색 응답 상태: {response.status_code}")
    
    # HTML 파싱하여 PNU 찾기
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # PNU 또는 지번 정보 찾기
    # 실제로는 JavaScript로 처리되므로 다른 방법 필요
    
except Exception as e:
    print(f"오류: {e}")

print("\n" + "="*80)
print("\n대안: 다양한 지번 형식으로 API 테스트")
print("="*80)

import xml.etree.ElementTree as ET

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

# 부산 강서구 대저1동의 법정동 코드 확인 필요
# 가능한 조합들 테스트
test_cases = [
    # (시군구, 법정동, 산여부, 본번, 부번)
    ("26440", "10400", "0", "790", "0"),      # 대저1동
    ("26440", "10400", "0", "0790", "0000"),  # 0 패딩
    ("26440", "10500", "0", "790", "0"),      # 대저2동
    ("26440", "10300", "0", "790", "0"),      # 대저동
]

for sigungu, bjdong, platGb, bun, ji in test_cases:
    print(f"\n테스트: 시군구={sigungu}, 법정동={bjdong}, 구분={platGb}, 본번={bun}, 부번={ji}")
    
    q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=100"
    
    try:
        res = session.get(connector_url, params={'url': q}, timeout=10)
        if res.status_code == 200 and '<response>' in res.text:
            root = ET.fromstring(res.text)
            
            # 에러 메시지 확인
            result_code = root.findtext('.//resultCode', '')
            result_msg = root.findtext('.//resultMsg', '')
            
            items = root.findall('.//item')
            print(f"  결과 코드: {result_code}, 메시지: {result_msg}")
            print(f"  발견된 건물 수: {len(items)}")
            
            if items:
                for idx, item in enumerate(items[:3], 1):  # 처음 3개만
                    print(f"    건물 {idx}: {item.findtext('bldNm', '')} / {item.findtext('dongNm', '')} / {item.findtext('mainPurpsCdNm', '')}")
        else:
            print(f"  API 호출 실패: {res.status_code}")
    except Exception as e:
        print(f"  오류: {e}")
