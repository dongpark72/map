"""
서울 강동구 명일동 56 - 층별 데이터 테스트
PNU: 1174010100100560000
"""
import requests
import xml.etree.ElementTree as ET
import urllib.parse

import sys

# 결과를 파일로 저장
f = open('myeongil_test_result.txt', 'w', encoding='utf-8')
sys.stdout = f

pnu = "1174010100100560000"

# PNU 파싱
sigungu = pnu[0:5]  # 11740
bjdong = pnu[5:10]   # 10100
pnu_land_type = pnu[10]  # 1
platGb = '0' if pnu_land_type == '1' else '1'  # 0 (대지)
bun = pnu[11:15]  # 0056
ji = pnu[15:19]   # 0008

print("=" * 80)
print(f"테스트 주소: 서울 강동구 명일동 56")
print(f"PNU: {pnu}")
print("=" * 80)
print(f"시군구코드: {sigungu}")
print(f"법정동코드: {bjdong}")
print(f"대지구분코드: {platGb} (PNU[10]={pnu_land_type})")
print(f"번: {bun}")
print(f"지: {ji}")
print("=" * 80)

# API 설정
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
enc_key = urllib.parse.quote(api_key)

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

# 1. 일반표제부 조회 (건물 기본 정보)
print("\n[1] 일반표제부 조회 (건물 기본 정보)")
api_url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
query = f"{api_url_title}^serviceKey={enc_key}|numOfRows=10|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"

try:
    res = session.get(connector_url, params={'url': query}, timeout=10)
    print(f"   Status: {res.status_code}")
    
    if res.status_code == 200 and '<item>' in res.text:
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        print(f"   ✓ 건물 정보 발견: {len(items)}개")
        
        if items:
            item = items[0]
            pk = item.find('mgmBldrgstPk')
            bldNm = item.find('bldNm')
            totArea = item.find('totArea')
            
            if pk is not None and pk.text:
                mgm_pk = pk.text
                print(f"   - 관리번호(PK): {mgm_pk}")
                print(f"   - 건물명: {bldNm.text if bldNm is not None and bldNm.text else 'N/A'}")
                print(f"   - 연면적: {totArea.text if totArea is not None and totArea.text else 'N/A'}㎡")
                
                # 2. 층별 정보 조회
                print(f"\n[2] 층별 정보 조회 (PK: {mgm_pk})")
                api_url_flr = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
                query_flr = f"{api_url_flr}^serviceKey={enc_key}|numOfRows=300|mgmBldrgstPk={mgm_pk}"
                
                res_flr = session.get(connector_url, params={'url': query_flr}, timeout=10)
                print(f"   Status: {res_flr.status_code}")
                
                if res_flr.status_code == 200 and '<item>' in res_flr.text:
                    root_flr = ET.fromstring(res_flr.text)
                    floor_items = root_flr.findall('.//item')
                    print(f"   ✓✓ 층별 데이터 발견: {len(floor_items)}개 층")
                    
                    if floor_items:
                        print(f"\n   층별 정보 샘플 (처음 5개):")
                        for idx, f_item in enumerate(floor_items[:5]):
                            flr_gb = f_item.find('flrGbCdNm')
                            flr_no = f_item.find('flrNoNm')
                            area = f_item.find('area')
                            purps = f_item.find('mainPurpsCdNm')
                            
                            print(f"   {idx+1}. {flr_gb.text if flr_gb is not None else 'N/A'} "
                                  f"{flr_no.text if flr_no is not None else 'N/A'}층 - "
                                  f"{area.text if area is not None else 'N/A'}㎡ - "
                                  f"{purps.text if purps is not None else 'N/A'}")
                        
                        print(f"\n   ✅ 성공! 이 건물은 층별 데이터가 있습니다!")
                    else:
                        print(f"   ⚠️ 응답은 있지만 층별 데이터가 비어있습니다.")
                else:
                    print(f"   ❌ 층별 데이터 없음")
                    print(f"   응답 샘플: {res_flr.text[:200]}")
    else:
        print(f"   ❌ 건물 정보 없음")
        print(f"   응답 샘플: {res.text[:200]}")
        
except Exception as e:
    print(f"   ❌ 오류: {e}")

print("\n" + "=" * 80)
