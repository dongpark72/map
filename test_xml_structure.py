"""
건축물대장 API 응답 구조 상세 분석
"""
import requests
import xml.etree.ElementTree as ET

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

# 테스트용으로 알려진 건물이 있는 주소 사용
# 예: 서울시청 (서울특별시 중구 세종대로 110)
# PNU: 1114010100100110000

test_cases = [
    {
        'name': '서울시청 (테스트)',
        'sigungu': '11140',
        'bjdong': '10100',
        'platGb': '0',
        'bun': '110',
        'ji': '0'
    },
    {
        'name': '부산 강서구 대저1동 790',
        'sigungu': '26440',
        'bjdong': '10400',
        'platGb': '0',
        'bun': '790',
        'ji': '0'
    }
]

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
session.headers.update(headers)

for test in test_cases:
    print("\n" + "="*80)
    print(f"테스트: {test['name']}")
    print("="*80)
    
    sigungu = test['sigungu']
    bjdong = test['bjdong']
    platGb = test['platGb']
    bun = test['bun']
    ji = test['ji']
    
    print(f"파라미터: 시군구={sigungu}, 법정동={bjdong}, 구분={platGb}, 본번={bun}, 부번={ji}")
    
    # 표제부 API
    api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
    q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=100"
    
    try:
        res = session.get(connector_url, params={'url': q}, timeout=10)
        print(f"\n응답 상태: {res.status_code}")
        print(f"응답 길이: {len(res.text)} bytes")
        
        if res.status_code == 200:
            # XML 전체 출력 (처음 2000자)
            print(f"\nXML 응답 (처음 2000자):")
            print("-"*80)
            print(res.text[:2000])
            print("-"*80)
            
            if '<response>' in res.text:
                root = ET.fromstring(res.text)
                
                # 모든 태그 출력
                print(f"\nXML 구조 분석:")
                for child in root.iter():
                    if child.text and child.text.strip():
                        print(f"  {child.tag}: {child.text.strip()[:100]}")
                
                items = root.findall('.//item')
                print(f"\n발견된 item 수: {len(items)}")
                
                if items:
                    print(f"\n첫 번째 item의 모든 필드:")
                    for elem in items[0]:
                        print(f"  {elem.tag}: {elem.text}")
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
