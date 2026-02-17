import requests
import xml.etree.ElementTree as ET

pnu = "2642010200103690009"
sigunguCd = pnu[0:5]
bjdongCd = pnu[5:10]
platGbCd = '0' if pnu[10] == '1' else '1'
bun = pnu[11:15]
ji = pnu[15:19]

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

# Try with 100 rows to be safe
q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={platGbCd}|bun={bun}|ji={ji}|numOfRows=100"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
}

try:
    res = requests.get(connector_url, params={'url': q}, headers=headers, timeout=15)
    print(f"Status: {res.status_code}")
    print("Response (first 2000 chars):")
    print(res.text[:2000])
    
    if '<item>' in res.text:
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        print(f"\nTOTAL ITEMS FOUND: {len(items)}")
        for i, item in enumerate(items):
            bldNm = item.find('bldNm').text if item.find('bldNm') is not None else 'N/A'
            dongNm = item.find('dongNm').text if item.find('dongNm') is not None else 'N/A'
            print(f"[{i}] Building: {bldNm}, Dong: {dongNm}")
    else:
        print("\nNO ITEMS FOUND IN RESPONSE")
except Exception as e:
    print(f"Error: {e}")
