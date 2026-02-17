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

for plat in ['0', '1']:
    print(f"\n--- Testing platGbCd={plat} ---")
    # Try with raw bun/ji
    q = f"{title_api}^serviceKey={api_key}|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={plat}|bun={bun}|ji={ji}|numOfRows=10"
    res = requests.get(connector_url, params={'url': q})
    print(f"Raw Bun/Ji Result: {'Found items' if '<item>' in res.text else 'No items'}")
    
    # Try with integer bun/ji
    q_int = f"{title_api}^serviceKey={api_key}|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={plat}|bun={int(bun)}|ji={int(ji)}|numOfRows=10"
    res_int = requests.get(connector_url, params={'url': q_int})
    print(f"Int Bun/Ji Result: {'Found items' if '<item>' in res_int.text else 'No items'}")
    if '<item>' in res_int.text:
        root = ET.fromstring(res_int.text)
        for it in root.findall('.//item'):
            print(f"  Building: {it.find('bldNm').text}, Dong: {it.find('dongNm').text}")
