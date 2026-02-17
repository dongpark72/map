import requests
import xml.etree.ElementTree as ET

pnu = "2644010100107900000" # 부산 강서구 대저1동 790
sigunguCd = pnu[0:5]
bjdongCd = pnu[5:10]
platGbCd = '0' if pnu[10] == '1' else '1'
bun = str(int(pnu[11:15]))
ji = str(int(pnu[15:19]))

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

# 1. 표제부 정보 (getBrTitleInfo)
title_api = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
q_title = f"{title_api}^serviceKey={api_key}|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={platGbCd}|bun={bun}|ji={ji}|numOfRows=100"

print(f"--- getBrTitleInfo ---")
res = requests.get(connector_url, params={'url': q_title})
if '<item>' in res.text:
    root = ET.fromstring(res.text)
    items = root.findall('.//item')
    print(f"Found {len(items)} items in Title Info.")
    for it in items:
        print(f"Building: {it.find('bldNm').text if it.find('bldNm') is not None else ''}, Dong: {it.find('dongNm').text if it.find('dongNm') is not None else ''}")
else:
    print("No items found in Title Info.")

# 2. 총괄표제부 정보 (getBrRecapTitleInfo) - 단지형인 경우
recap_api = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
q_recap = f"{recap_api}^serviceKey={api_key}|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={platGbCd}|bun={bun}|ji={ji}|numOfRows=100"

print(f"\n--- getBrRecapTitleInfo ---")
res = requests.get(connector_url, params={'url': q_recap})
if '<item>' in res.text:
    root = ET.fromstring(res.text)
    items = root.findall('.//item')
    print(f"Found {len(items)} items in Recap Title Info.")
else:
    print("No items found in Recap Title Info.")
