import requests
import xml.etree.ElementTree as ET

pnu = "2644010100107900000"
sigunguCd = pnu[0:5]
bjdongCd = pnu[5:10]
bun = "0790"
ji = "0000"

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
title_api = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

q = f"{title_api}^serviceKey={api_key}|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd=0|bun={bun}|ji={ji}|numOfRows=100"
res = requests.get(connector_url, params={'url': q})
if '<item>' in res.text:
    root = ET.fromstring(res.text)
    items = root.findall('.//item')
    print(f"TOTAL ITEMS FOUND: {len(items)}")
    for i, it in enumerate(items):
        bldNm = it.find('bldNm').text if it.find('bldNm') is not None else 'N/A'
        dongNm = it.find('dongNm').text if it.find('dongNm') is not None else 'N/A'
        mainPurps = it.find('mainPurpsCdNm').text if it.find('mainPurpsCdNm') is not None else 'N/A'
        print(f"[{i}] {bldNm} | {dongNm} | {mainPurps}")
else:
    print("NO ITEMS FOUND")
