"""
일반건축물 기본개요 API (getBrBasisOulnInfo) 테스트
"""
import requests
import xml.etree.ElementTree as ET

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

# 테스트 케이스
test_cases = [
    {
        'name': '부산 강서구 대저1동 790',
        'sigungu': '26440',
        'bjdong': '10400',
        'platGb': '0',
        'bun': '790',
        'ji': '0'
    },
    {
        'name': '서울시청 (테스트)',
        'sigungu': '11140',
        'bjdong': '10100',
        'platGb': '0',
        'bun': '110',
        'ji': '0'
    }
]

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
session.headers.update(headers)

print("="*80)
print("일반건축물 기본개요 API (getBrBasisOulnInfo) 테스트")
print("="*80)

for test in test_cases:
    print(f"\n{'='*80}")
    print(f"테스트: {test['name']}")
    print('='*80)
    
    sigungu = test['sigungu']
    bjdong = test['bjdong']
    platGb = test['platGb']
    bun = test['bun']
    ji = test['ji']
    
    print(f"파라미터: 시군구={sigungu}, 법정동={bjdong}, 구분={platGb}, 본번={bun}, 부번={ji}")
    
    # 일반건축물 기본개요 API
    api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrBasisOulnInfo"
    q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=100"
    
    try:
        res = session.get(connector_url, params={'url': q}, timeout=10)
        print(f"\n응답 상태: {res.status_code}")
        print(f"응답 길이: {len(res.text)} bytes")
        
        if res.status_code == 200 and '<response>' in res.text:
            # XML 응답 일부 출력
            print(f"\nXML 응답 (처음 1500자):")
            print("-"*80)
            print(res.text[:1500])
            print("-"*80)
            
            root = ET.fromstring(res.text)
            
            # 결과 코드 확인
            result_code = root.findtext('.//resultCode', '')
            result_msg = root.findtext('.//resultMsg', '')
            total_count = root.findtext('.//totalCount', '0')
            
            print(f"\n결과 코드: {result_code}")
            print(f"결과 메시지: {result_msg}")
            print(f"총 건수: {total_count}")
            
            items = root.findall('.//item')
            print(f"발견된 item 수: {len(items)}")
            
            if items:
                print(f"\n건물 목록:")
                for idx, item in enumerate(items, 1):
                    bld_nm = item.findtext('bldNm', '')
                    dong_nm = item.findtext('dongNm', '')
                    main_purps = item.findtext('mainPurpsCdNm', '')
                    tot_area = item.findtext('totArea', '')
                    arch_area = item.findtext('archArea', '')
                    main_strct = item.findtext('mainStrctCdNm', '')
                    
                    print(f"\n  [{idx}] 건물 정보:")
                    print(f"      건물명: {bld_nm}")
                    print(f"      동명칭: {dong_nm}")
                    print(f"      주용도: {main_purps}")
                    print(f"      주구조: {main_strct}")
                    print(f"      연면적: {tot_area} m²")
                    print(f"      건축면적: {arch_area} m²")
                
                # 첫 번째 item의 모든 필드 출력
                if len(items) > 0:
                    print(f"\n첫 번째 건물의 모든 필드:")
                    print("-"*80)
                    for elem in items[0]:
                        if elem.text:
                            print(f"  {elem.tag}: {elem.text}")
            else:
                print("\n건물 정보 없음")
        else:
            print(f"API 호출 실패: {res.status_code}")
            print(f"응답: {res.text[:500]}")
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
print("테스트 완료")
print("="*80)
