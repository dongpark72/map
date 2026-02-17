
import requests
import xml.etree.ElementTree as ET

def check_318():
    url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    q = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo^serviceKey=eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==|platGbCd=0|sigunguCd=26440|bjdongCd=10400|bun=0318"
    r = requests.get(url, params={'url': q})
    root = ET.fromstring(r.text)
    for it in root.findall('.//item'):
        ji = it.find('ji').text if it.find('ji') is not None else ""
        bld = it.find('bldNm').text if it.find('bldNm') is not None else ""
        print(f"Ji:{ji} Name:{bld}")

if __name__ == "__main__":
    check_318()
