"""
명일동 56번지 상세 API 테스트
"""
import requests
import xml.etree.ElementTree as ET
import urllib.parse
import sys

f = open('myeongil_detailed_test.txt', 'w', encoding='utf-8')
sys.stdout = f

pnu = "1174010100100560000"
sigungu = "11740"
bjdong = "10100"
platGb = "0"
bun = "0056"
ji = "0000"

api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
enc_key = urllib.parse.quote(api_key)
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
session = requests.Session()

def call_api(url, params):
    query = f"{url}^serviceKey={enc_key}|" + "|".join([f"{k}={v}" for k, v in params.items()])
    res = session.get(connector_url, params={'url': query}, timeout=10)
    return res

apis = {
    "RecapTitle": "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo",
    "Title": "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo",
    "Basis": "http://apis.data.go.kr/1613000/BldRgstHubService/getBrBasisOulnInfo"
}

print(f"Testing PNU: {pnu}")

for name, url in apis.items():
    print(f"\n--- Testing {name} ---")
    res = call_api(url, {"sigunguCd": sigungu, "bjdongCd": bjdong, "platGbCd": platGb, "bun": bun, "ji": ji, "numOfRows": 100})
    print(f"Status: {res.status_code}")
    if "<item>" in res.text:
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        print(f"Found {len(items)} items")
        for i, item in enumerate(items[:5]):
            pk = item.findtext('mgmBldrgstPk')
            bld_nm = item.findtext('bldNm')
            dong_nm = item.findtext('dongNm')
            print(f"  {i+1}. PK={pk}, Name={bld_nm}, Dong={dong_nm}")
            
            # For each PK, try to get Floor Info
            if pk:
                print(f"     Trying Floor Info for PK={pk}...")
                flr_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
                res_flr = call_api(flr_url, {"mgmBldrgstPk": pk, "numOfRows": 10})
                if "<item>" in res_flr.text:
                    flr_items = ET.fromstring(res_flr.text).findall('.//item')
                    print(f"     ✅ Found {len(flr_items)} floors")
                else:
                    print(f"     ❌ No floors")
    else:
        print("No items found")

f.close()
