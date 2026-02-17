import requests
import xml.etree.ElementTree as ET

pnu = "2642010200103690009"
sigunguCd = pnu[0:5]
bjdongCd = pnu[5:10]
bun = pnu[11:15]
ji = pnu[15:19]

print(f"Original PNU parts: {sigunguCd}, {bjdongCd}, {bun}, {ji}")

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

# Try with zeros as in the original code
q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd=0|bun={bun}|ji={ji}|numOfRows=100"
res = requests.get(connector_url, params={'url': q})
print(f"Result with zeros: {res.text[:500]}")
