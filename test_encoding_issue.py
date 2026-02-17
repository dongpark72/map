"""
실거래가 API 응답의 한글 인코딩 문제 테스트
"""
import requests
import xml.etree.ElementTree as ET
import sys

# 테스트할 PNU (부산 사상구 감전동 147-3)
test_pnu = "2641010800101470003"
sigungu_cd = test_pnu[:5]  # "26410"

# API 설정
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url = "http://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade"

# 공공데이터포털 API 키 (환경변수에서 가져오기)
import os
from dotenv import load_dotenv
load_dotenv()

api_keys = [
    os.getenv('PUBLIC_DATA_KEY_1'),
    os.getenv('PUBLIC_DATA_KEY_2'),
    os.getenv('PUBLIC_DATA_KEY_3')
]

# 최근 1개월만 테스트
from datetime import datetime
now = datetime.now()
test_month = f"{now.year}{now.month:02d}"

print(f"=== 실거래가 API 인코딩 테스트 ===")
print(f"PNU: {test_pnu}")
print(f"시군구코드: {sigungu_cd}")
print(f"테스트 월: {test_month}")
print(f"API URL: {api_url}")
print()

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

for idx, api_key in enumerate(api_keys, 1):
    if not api_key:
        print(f"[키 {idx}] 설정되지 않음")
        continue
    
    print(f"\n[키 {idx}] 테스트 중...")
    
    import urllib.parse
    enc_key = urllib.parse.quote(api_key)
    query = f"{api_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={test_month}"
    
    try:
        res = session.get(connector_url, params={'url': query}, timeout=10)
        print(f"  상태 코드: {res.status_code}")
        print(f"  Content-Type: {res.headers.get('Content-Type', 'N/A')}")
        print(f"  인코딩: {res.encoding}")
        
        # 응답 텍스트의 처음 500자 출력
        print(f"\n  응답 내용 (처음 500자):")
        print(f"  {res.text[:500]}")
        
        # XML 파싱 시도
        if res.status_code == 200 and "<item>" in res.text:
            try:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                print(f"\n  파싱된 아이템 수: {len(items)}")
                
                if items:
                    # 첫 번째 아이템의 모든 필드 출력
                    print(f"\n  첫 번째 아이템의 필드:")
                    item = items[0]
                    for child in item:
                        tag = child.tag
                        text = child.text.strip() if child.text else ''
                        print(f"    {tag}: {text}")
                        
                        # 한글이 깨졌는지 확인
                        if text:
                            try:
                                # UTF-8로 인코딩 가능한지 확인
                                text.encode('utf-8')
                                has_korean = any('\uac00' <= c <= '\ud7a3' for c in text)
                                if has_korean:
                                    print(f"      → 한글 포함됨 (정상)")
                            except UnicodeEncodeError:
                                print(f"      → 인코딩 오류 발생!")
                
                # 성공하면 더 이상 다른 키 테스트 안 함
                break
                
            except ET.ParseError as e:
                print(f"  XML 파싱 오류: {e}")
        elif res.status_code == 200:
            print(f"  응답에 <item> 태그 없음")
            # 에러 메시지 확인
            if "<returnReasonCode>" in res.text:
                try:
                    root = ET.fromstring(res.text)
                    code = root.find('.//returnReasonCode')
                    msg = root.find('.//returnAuthMsg')
                    if code is not None:
                        print(f"  에러 코드: {code.text}")
                    if msg is not None:
                        print(f"  에러 메시지: {msg.text}")
                except:
                    pass
        
    except Exception as e:
        print(f"  오류 발생: {e}")
        import traceback
        traceback.print_exc()

print("\n=== 테스트 완료 ===")
