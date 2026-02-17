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
    
    enc_key = urllib.parse.quote(API_KEY)
    q_elvt = f"{api_url_elvt}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={platGbCd}|bun={bun}|ji={ji}"
    
    print(f"Testing PNU: {pnu} (Sigungu:{sigunguCd}, Bjdong:{bjdongCd}, Bun:{bun}, Ji:{ji})")
    try:
        res = requests.get(connector_url, params={'url': q_elvt}, timeout=10)
        if res.status_code == 200:
            if "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                print(f"  SUCCESS! Found {len(items)} elevator records.")
                for item in items:
                    dong = item.findtext('dongNm', 'N/A')
                    gb = item.findtext('elvtGbCdNm', 'N/A')
                    cnt = item.findtext('elvtCnt', '0')
                    print(f"    - Dong: {dong}, Type: {gb}, Count: {cnt}")
                return True
            else:
                print("  No elevator data found.")
        else:
            print(f"  API Error: {res.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    return False

# PNUs to try
pnus = [
    "2635010400118290000", # Haeundae LCT
    "2653010200103690009", # Deokpo-dong 369-9
    "2644010400107900000", # Daejeo 1-dong 790
    "1168010100107370000", # GFC (Try again)
    "1171010100100290000", # Lotte World Tower (Try again)
]

for p in pnus:
    if check_elevator(p):
        print(f"\nFOUND ONE: {p}")
        break
