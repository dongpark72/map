"""
공공데이터포털 API 직접 테스트 - 웹브라우저로 확인 가능한 URL 생성
"""
import urllib.parse

# API 키
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
encoded_key = urllib.parse.quote(api_key)

# 테스트할 건물 정보
sigungu = "26200"
bjdong = "12100"
platGb = "0"
bun = "0318"
ji = "0045"
pk = "10311100190464"

print("=" * 80)
print("공공데이터포털 API 직접 테스트 URL")
print("=" * 80)

# 1. 일반표제부 (건물 기본 정보) - 이건 데이터 있음
url1 = f"http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo?serviceKey={encoded_key}&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}&numOfRows=10"
print("\n1. 일반표제부 (건물 기본 정보) - ✅ 데이터 있음")
print(f"   {url1}")

# 2. 층별개요 (층별 상세 정보) - 이건 데이터 없음
url2 = f"http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo?serviceKey={encoded_key}&mgmBldrgstPk={pk}&numOfRows=100"
print("\n2. 층별개요 (층별 상세 정보) - ❌ 데이터 없음")
print(f"   {url2}")

print("\n" + "=" * 80)
print("위 URL을 웹브라우저에 복사해서 직접 확인해보세요!")
print("=" * 80)
print("\n예상 결과:")
print("1번 URL: <item> 태그 안에 건물 정보가 있음")
print("2번 URL: <body></body> 비어있음 (데이터 없음)")
