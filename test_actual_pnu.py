"""
실제 애플리케이션에서 사용하는 방식으로 PNU를 생성하고 API 호출 테스트
"""
import requests
import xml.etree.ElementTree as ET

# 카카오 지오코더로 주소 검색 (애플리케이션과 동일한 방식)
def get_pnu_from_address(address):
    # 실제 앱에서 사용하는 카카오 API 키 필요
    # 여기서는 직접 PNU를 입력받거나 로그에서 확인한 PNU 사용
    pass

# 로그에서 확인하거나 사용자가 제공한 실제 PNU 사용
# 예: "부산광역시 강서구 대저1동 790"의 실제 PNU

print("="*80)
print("실제 사용 사례 테스트")
print("="*80)

# 사용자에게: 실제 앱에서 '강서구 대저1동 790'을 검색했을 때
# 서버 로그에 나타나는 PNU를 확인해주세요.
# 
# 또는 토지이음 웹사이트에서 직접 검색하여 PNU 확인:
# https://www.eum.go.kr/web/ar/lu/luLandDet.jsp

print("\n토지이음에서 '부산광역시 강서구 대저1동 790'을 검색하면:")
print("URL에 pnu 파라미터가 표시됩니다.")
print("\n예시: https://www.eum.go.kr/web/ar/lu/luLandDet.jsp?pnu=XXXXXXXXXXXXXXXXXXX")
print("\n해당 PNU를 확인한 후, 아래 코드에서 테스트할 수 있습니다.")

# 테스트용 PNU들 (실제 확인 필요)
test_pnus = [
    "2644010400107900000",  # 추정 PNU
]

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
session.headers.update(headers)

for pnu in test_pnus:
    print(f"\n{'='*80}")
    print(f"PNU: {pnu}")
    print('='*80)
    
    sigungu = pnu[0:5]
    bjdong = pnu[5:10]
    platGb = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15]))
    ji = str(int(pnu[15:19]))
    
    print(f"파싱 결과: 시군구={sigungu}, 법정동={bjdong}, 구분={platGb}, 본번={bun}, 부번={ji}")
    
    # 표제부 API 테스트
    api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
    q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=100"
    
    print(f"\n[표제부 API] 호출 중...")
    try:
        res = session.get(connector_url, params={'url': q}, timeout=10)
        if res.status_code == 200 and '<response>' in res.text:
            root = ET.fromstring(res.text)
            items = root.findall('.//item')
            total_count = root.findtext('.//totalCount', '0')
            
            print(f"  총 건수: {total_count}")
            print(f"  발견된 item 수: {len(items)}")
            
            if items:
                print(f"\n  건물 목록:")
                for idx, item in enumerate(items, 1):
                    bld_nm = item.findtext('bldNm', '')
                    dong_nm = item.findtext('dongNm', '')
                    main_purps = item.findtext('mainPurpsCdNm', '')
                    tot_area = item.findtext('totArea', '')
                    print(f"    {idx}. 건물명: {bld_nm}, 동명칭: {dong_nm}, 용도: {main_purps}, 연면적: {tot_area}")
            else:
                print("  건물 없음")
                # 응답 내용 일부 출력
                print(f"\n  응답 내용 (처음 1000자):")
                print(res.text[:1000])
        else:
            print(f"  API 호출 실패: {res.status_code}")
    except Exception as e:
        print(f"  오류: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
print("참고: 실제 PNU는 애플리케이션에서 검색 후 서버 로그를 확인하거나")
print("토지이음 웹사이트에서 직접 검색하여 URL의 pnu 파라미터를 확인하세요.")
print("="*80)
