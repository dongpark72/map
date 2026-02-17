import requests
import xml.etree.ElementTree as ET

# 강서구 대저1동 790의 PNU 계산
# 부산광역시 강서구 = 26440
# 대저1동 = 10400
# 790번지 = 0790, 0000
pnu = "2644010400107900000"

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

sigungu = pnu[0:5]
bjdong = pnu[5:10]
platGb = '0' if pnu[10] == '1' else '1'
bun = str(int(pnu[11:15]))
ji = str(int(pnu[15:19]))

print(f"PNU: {pnu}")
print(f"시군구: {sigungu}, 법정동: {bjdong}, 구분: {platGb}, 본번: {bun}, 부번: {ji}")
print("\n" + "="*80)

# 1. 총괄표제부 API 테스트
print("\n[1] 총괄표제부 API (getBrRecapTitleInfo) 테스트:")
print("-"*80)
recap_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
q_recap = f"{recap_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=100"

try:
    res_recap = requests.get(connector_url, params={'url': q_recap}, timeout=10)
    if res_recap.status_code == 200 and '<response>' in res_recap.text:
        root = ET.fromstring(res_recap.text)
        items = root.findall('.//item')
        print(f"발견된 건물 수: {len(items)}")
        
        for idx, item in enumerate(items, 1):
            print(f"\n건물 {idx}:")
            print(f"  건물명: {item.findtext('bldNm', '')}")
            print(f"  동명칭: {item.findtext('dongNm', '')}")
            print(f"  주용도: {item.findtext('mainPurpsCdNm', '')}")
    else:
        print(f"API 호출 실패: status={res_recap.status_code}")
        print(f"응답 미리보기: {res_recap.text[:500]}")
except Exception as e:
    print(f"오류 발생: {e}")

print("\n" + "="*80)

# 2. 표제부 API 테스트
print("\n[2] 표제부 API (getBrTitleInfo) 테스트:")
print("-"*80)
title_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
q_title = f"{title_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=100"

try:
    res_title = requests.get(connector_url, params={'url': q_title}, timeout=10)
    if res_title.status_code == 200 and '<response>' in res_title.text:
        root = ET.fromstring(res_title.text)
        items = root.findall('.//item')
        print(f"발견된 건물 수: {len(items)}")
        
        for idx, item in enumerate(items, 1):
            print(f"\n건물 {idx}:")
            print(f"  건물명: {item.findtext('bldNm', '')}")
            print(f"  동명칭: {item.findtext('dongNm', '')}")
            print(f"  주용도: {item.findtext('mainPurpsCdNm', '')}")
            print(f"  연면적: {item.findtext('totArea', '')}")
    else:
        print(f"API 호출 실패: status={res_title.status_code}")
        print(f"응답 미리보기: {res_title.text[:500]}")
except Exception as e:
    print(f"오류 발생: {e}")

print("\n" + "="*80)
print("\n결론: 두 API의 반환 건물 수를 비교하여 어느 것이 모든 건물을 반환하는지 확인하세요.")
