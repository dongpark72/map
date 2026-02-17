import requests
import urllib.parse
import xml.etree.ElementTree as ET

API_KEY = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url_elvt = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrElvtInfo"

def check_elevator(pnu):
    sigunguCd = pnu[0:5]
    bjdongCd = pnu[5:10]
    platGbCd = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15]))
    ji = str(int(pnu[15:19]))
    
    # Direct call to public data portal
    direct_params = {
        'serviceKey': API_KEY,
        'numOfRows': 999,
        'pageNo': 1,
        'sigunguCd': sigunguCd,
        'bjdongCd': bjdongCd,
        'platGbCd': platGbCd,
        'bun': bun,
        'ji': ji
    }
    
    print(f"Testing PNU: {pnu}")
    try:
        res = requests.get(api_url_elvt, params=direct_params, timeout=10)
        if res.status_code == 200:
            if "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                print(f"  FOUND {len(items)} elevator records!")
                for item in items:
                    dong = item.findtext('dongNm', 'N/A')
                    gb = item.findtext('elvtGbCdNm', 'N/A')
                    cnt = item.findtext('elvtCnt', '0')
                    print(f"    - Dong: {dong}, Type: {gb}, Count: {cnt}")
                return True
            else:
                print("  No elevator data.")
                print(f"  Debug Response: {res.text[:200]}")
        else:
            print(f"  Error: {res.status_code}")
            print(f"  Debug Response: {res.text[:200]}")
    except Exception as e:
        print(f"  Exception: {e}")
    return False

pnus = [
    "2623010100105030015", # Lotte Dept Store Busan
    "2635010500115150000", # Shinsegae Centum City
    "1114011400100430000", # Seoul City Hall?
    "1171010100100290000", # Lotte World Tower
]

for p in pnus:
    if check_elevator(p):
        print(f"\nSUCCESS! PNU: {p}")
        break
