import requests
import xml.etree.ElementTree as ET

pnu = "2642010200103690009"
sigunguCd = pnu[0:5]
bjdongCd = pnu[5:10]

# Try with only Sigungu
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigunguCd}|numOfRows=10"
res = requests.get(connector_url, params={'url': q})
print(f"Sample results for Sigungu {sigunguCd}:")
if '<item>' in res.text:
    root = ET.fromstring(res.text)
    for item in root.findall('.//item'):
        addr = item.find('platPlc').text if item.find('platPlc') is not None else 'N/A'
        bun = item.find('bun').text if item.find('bun') is not None else 'N/A'
        ji = item.find('ji').text if item.find('ji') is not None else 'N/A'
        bjdong = item.find('bjdongCd').text if item.find('bjdongCd') is not None else 'N/A'
        print(f"Addr: {addr}, Bjdong: {bjdong}, Bun: {bun}, Ji: {ji}")
else:
    print("No items found.")
    print(res.text[:500])
