"""
사상구 감전동 147-3 주소의 실거래가 데이터 디버깅
"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

# API 키 설정
API_KEY = os.getenv('PUBLIC_DATA_KEY_1', 'your_api_key_here')

# 사상구 감전동 147-3의 PNU 계산
# 부산광역시 사상구 감전동: 26530
# 산: 2 (일반: 1)
# 본번: 0147
# 부번: 0003
# PNU = 2653010300101470003

pnu = "2653010300101470003"
sigungu_cd = pnu[:5]  # 26530

print("=" * 80)
print("사상구 감전동 147-3 실거래가 데이터 디버깅")
print("=" * 80)
print(f"PNU: {pnu}")
print(f"시군구코드: {sigungu_cd}")
print()

# 현재 시점부터 최근 24개월
now = datetime.now()
months = []
curr_y, curr_m = now.year, now.month
for i in range(24):
    m = curr_m - i
    y = curr_y
    while m <= 0:
        m += 12
        y -= 1
    months.append(f"{y}{m:02d}")

print(f"조회 기간: {months[-1]} ~ {months[0]} (최근 24개월)")
print()

# 7가지 실거래가 유형 테스트
api_types = {
    'factory': 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade',
    'land': 'http://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade',
    'apt': 'http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev',
    'offi': 'http://apis.data.go.kr/1613000/RTMSDataSvcOffiTrade/getRTMSDataSvcOffiTrade',
    'row': 'http://apis.data.go.kr/1613000/RTMSDataSvcRHTrade/getRTMSDataSvcRHTrade',
    'detached': 'http://apis.data.go.kr/1613000/RTMSDataSvcSHTrade/getRTMSDataSvcSHTrade',
    'biz': 'http://apis.data.go.kr/1613000/RTMSDataSvcNrgTrade/getRTMSDataSvcNrgTrade',
}

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"

def test_api_type(type_name, api_url, test_months):
    """특정 유형의 실거래가 API 테스트"""
    print(f"\n{'='*80}")
    print(f"[{type_name.upper()}] 실거래가 조회")
    print(f"{'='*80}")
    
    total_items = 0
    found_months = []
    
    for month in test_months[:6]:  # 최근 6개월만 테스트
        query = f"{api_url}^serviceKey={API_KEY}|LAWD_CD={sigungu_cd}|DEAL_YMD={month}"
        
        try:
            response = requests.get(connector_url, params={'url': query}, timeout=10)
            
            if response.status_code == 200:
                if "<item>" in response.text:
                    root = ET.fromstring(response.text)
                    items = root.findall('.//item')
                    
                    if items:
                        print(f"  {month}: {len(items)}건 발견")
                        total_items += len(items)
                        found_months.append(month)
                        
                        # 첫 번째 항목의 상세 정보 출력
                        if len(items) > 0:
                            item = items[0]
                            print(f"    샘플 데이터:")
                            for child in item:
                                if child.text and child.text.strip():
                                    print(f"      {child.tag}: {child.text.strip()}")
                    else:
                        print(f"  {month}: 데이터 없음")
                elif "<items/>" in response.text or "<items />" in response.text:
                    print(f"  {month}: 데이터 없음 (빈 응답)")
                else:
                    print(f"  {month}: 응답 파싱 실패")
                    # 에러 메시지 확인
                    if "<returnReasonCode>" in response.text:
                        root = ET.fromstring(response.text)
                        code = root.find('.//returnReasonCode')
                        msg = root.find('.//returnAuthMsg')
                        if code is not None:
                            print(f"    에러 코드: {code.text}")
                        if msg is not None:
                            print(f"    에러 메시지: {msg.text}")
            else:
                print(f"  {month}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  {month}: 오류 - {e}")
    
    print(f"\n총 {total_items}건 발견 ({len(found_months)}개월)")
    return total_items

# 모든 유형 테스트
results = {}
for type_name, api_url in api_types.items():
    count = test_api_type(type_name, api_url, months)
    results[type_name] = count

# 결과 요약
print("\n" + "=" * 80)
print("결과 요약")
print("=" * 80)
for type_name, count in results.items():
    status = "✓" if count > 0 else "✗"
    print(f"{status} {type_name:12s}: {count:4d}건")

print("\n" + "=" * 80)
if sum(results.values()) == 0:
    print("⚠️  모든 유형에서 데이터가 없습니다.")
    print("\n가능한 원인:")
    print("1. 해당 지역에 실제로 최근 2년 내 거래가 없음")
    print("2. PNU가 잘못 계산됨")
    print("3. API 키 문제")
    print("4. 시군구 코드가 잘못됨")
else:
    print(f"✓ 총 {sum(results.values())}건의 실거래가 데이터 발견")
    print("\n데이터가 있는 유형:")
    for type_name, count in results.items():
        if count > 0:
            print(f"  - {type_name}: {count}건")
