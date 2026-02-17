import requests
import xml.etree.ElementTree as ET
import urllib.parse

# API 설정
PUBLIC_DATA_KEYS = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368',
]

# 테스트용 PNU
# 서울특별시 강남구 역삼동 (실제 건물이 많은 위치)
test_pnu = '1168010100100010001'  # 강남구 역삼동

# PNU 파싱 함수
def parse_pnu(pnu):
    """19자리 PNU를 API 파라미터로 변환"""
    if len(pnu) != 19:
        raise ValueError(f"Invalid PNU length: {len(pnu)}, expected 19")
    
    sigunguCd = pnu[0:5]
    bjdongCd = pnu[5:10]
    platGbCd_num = pnu[10]
    bun = pnu[11:15]
    ji = pnu[15:19]
    
    # platGbCd 변환: 1=대지, 2=산
    platGbCd = '0' if platGbCd_num == '1' else '1'
    
    return {
        'sigunguCd': sigunguCd,
        'bjdongCd': bjdongCd,
        'platGbCd': platGbCd,
        'bun': bun,
        'ji': ji
    }

# 토지이음 커넥터 URL
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"

# 건축물대장 API 엔드포인트들
api_endpoints = {
    '총괄표제부': 'http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo',
    '일반표제부': 'http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo',
    '층별개요': 'http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo',
}

print("=" * 80)
print("V-World 건축물대장 API 층별정보 테스트")
print("=" * 80)
print(f"\n테스트 PNU: {test_pnu}")

try:
    params = parse_pnu(test_pnu)
    print(f"\n파싱된 파라미터:")
    for k, v in params.items():
        print(f"  {k}: {v}")
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    # 각 API 엔드포인트 테스트
    for api_name, api_url in api_endpoints.items():
        print(f"\n{'=' * 80}")
        print(f"[{api_name}] API 테스트")
        print(f"{'=' * 80}")
        
        for idx, api_key in enumerate(PUBLIC_DATA_KEYS, 1):
            print(f"\n[API Key {idx}] 시도 중...")
            enc_key = urllib.parse.quote(api_key)
            
            query = f"{api_url}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={params['sigunguCd']}|bjdongCd={params['bjdongCd']}|platGbCd={params['platGbCd']}|bun={params['bun']}|ji={params['ji']}"
            
            try:
                response = session.get(connector_url, params={'url': query}, timeout=10)
                
                if response.status_code == 200:
                    print(f"  상태 코드: {response.status_code}")
                    
                    # XML 파싱
                    try:
                        root = ET.fromstring(response.text)
                        
                        # 결과 코드 확인
                        result_code = root.find('.//resultCode')
                        result_msg = root.find('.//resultMsg')
                        
                        if result_code is not None:
                            print(f"  결과 코드: {result_code.text}")
                            print(f"  결과 메시지: {result_msg.text if result_msg is not None else 'N/A'}")
                        
                        # 아이템 개수 확인
                        items = root.findall('.//item')
                        print(f"  아이템 개수: {len(items)}")
                        
                        if items:
                            print(f"\n  [첫 번째 아이템 상세 정보]")
                            first_item = items[0]
                            
                            # 모든 필드 출력
                            for child in first_item:
                                tag = child.tag
                                text = child.text.strip() if child.text else ''
                                print(f"    {tag}: {text}")
                            
                            # 층별개요 API인 경우 특별히 층 정보 강조
                            if api_name == '층별개요':
                                print(f"\n  [층별 정보 필드]")
                                floor_fields = ['flrNo', 'flrNoNm', 'mainPurpsCdNm', 'area', 'strctCdNm']
                                for field in floor_fields:
                                    elem = first_item.find(field)
                                    if elem is not None:
                                        print(f"    {field}: {elem.text}")
                            
                            # 여러 아이템이 있으면 모두 표시
                            if len(items) > 1:
                                print(f"\n  [전체 {len(items)}개 아이템 요약]")
                                for i, item in enumerate(items, 1):
                                    if api_name == '층별개요':
                                        flr_no = item.find('flrNo')
                                        flr_nm = item.find('flrNoNm')
                                        area = item.find('area')
                                        print(f"    {i}. 층: {flr_nm.text if flr_nm is not None else 'N/A'} ({flr_no.text if flr_no is not None else 'N/A'}), 면적: {area.text if area is not None else 'N/A'}㎡")
                                    else:
                                        dong_nm = item.find('dongNm')
                                        bld_nm = item.find('bldNm')
                                        print(f"    {i}. 동명칭: {dong_nm.text if dong_nm is not None else 'N/A'}, 건물명: {bld_nm.text if bld_nm is not None else 'N/A'}")
                            
                            break  # 성공하면 다음 키 시도 안함
                        else:
                            print("  [WARN] 아이템 없음")
                            
                    except ET.ParseError as e:
                        print(f"  [ERROR] XML 파싱 오류: {e}")
                        print(f"  응답 내용 (처음 500자):\n{response.text[:500]}")
                else:
                    print(f"  [ERROR] HTTP 오류: {response.status_code}")
                    
            except requests.Timeout:
                print(f"  [ERROR] 타임아웃")
            except Exception as e:
                print(f"  [ERROR] 오류: {e}")

except Exception as e:
    print(f"\n[ERROR] 전체 오류: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("테스트 완료")
print("=" * 80)
