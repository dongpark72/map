import requests
import urllib.parse
import xml.etree.ElementTree as ET

API_KEY = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
api_url_elvt = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrElvtInfo"

def check_elevator_direct(pnu):
    sigunguCd = pnu[0:5]
    bjdongCd = pnu[5:10]
    platGbCd = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15]))
    ji = str(int(pnu[15:19]))
    
    params = {
        'serviceKey': API_KEY, # requests will urlencode this
        'numOfRows': 999,
        'pageNo': 1,
        'sigunguCd': sigunguCd,
        'bjdongCd': bjdongCd,
        'platGbCd': platGbCd,
        'bun': bun,
        'ji': ji
    }
    
    print(f"Testing PNU Direct: {pnu}")
    try:
        res = requests.get(api_url_elvt, params=params, timeout=10)
        print(f"  Status code: {res.status_code}")
        # print(f"  Response preview: {res.text[:200]}")
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
                print("  No elevator data in XML.")
        else:
            print(f"  API Error: {res.status_code}")
    except Exception as e:
        print(f"  Exception: {e}")
    return False

# PNUs
pnus = [
    "1171010100100290000", # Lotte World Tower
    "2635010500115150000", # Shinsegae Centum
    "2644010400107900000", # Daejeo 1-dong 790
]

for p in pnus:
    if check_elevator_direct(p):
        print(f"\nSUCCESS DIRECT! PNU: {p}")
        break
