import requests
import xml.etree.ElementTree as ET

pnu = "2642010200103690009"
sigunguCd = pnu[0:5]
bjdongCd = pnu[5:10]

# Try searching by sigungu+bjdong only with a small sample
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|numOfRows=10"
res = requests.get(connector_url, params={'url': q})
print(f"Sample results for {sigunguCd} {bjdongCd}:")
if '<item>' in res.text:
    root = ET.fromstring(res.text)
    for item in root.findall('.//item'):
        print(f"Addr: {item.find('platPlc').text if item.find('platPlc') is not None else ''}, Bun: {item.find('bun').text}, Ji: {item.find('ji').text}")
else:
    print("No items found.")
