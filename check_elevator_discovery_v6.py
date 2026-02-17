import requests
import urllib.parse
import xml.etree.ElementTree as ET

API_KEY = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url_elvt = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrElvtInfo"

def check_elevator(pnu, label=""):
    sigunguCd = pnu[0:5]
    bjdongCd = pnu[5:10]
    platGbCd = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15]))
    ji = str(int(pnu[15:19]))
    
    enc_key = urllib.parse.quote(API_KEY)
    q_elvt = f"{api_url_elvt}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={platGbCd}|bun={bun}|ji={ji}"
    
    print(f"Testing {label} PNU: {pnu}")
    try:
        # Try with HTTPS directly first to avoid proxy issues if any
        direct_url = f"https://apis.data.go.kr/1613000/BldRgstHubService/getBrElvtInfo"
        params = {
            'serviceKey': API_KEY,
            'numOfRows': 999,
            'pageNo': 1,
            'sigunguCd': sigunguCd,
            'bjdongCd': bjdongCd,
            'platGbCd': platGbCd,
            'bun': bun,
            'ji': ji
        }
        res = requests.get(direct_url, params=params, timeout=10)
        
        if res.status_code == 200 and "<item>" in res.text:
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
            # Fallback to proxy
            res_proxy = requests.get(connector_url, params={'url': q_elvt}, timeout=10)
            if res_proxy.status_code == 200 and "<item>" in res_proxy.text:
                root = ET.fromstring(res_proxy.text)
                items = root.findall('.//item')
                print(f"  FOUND {len(items)} elevator records via PROXY!")
                return True
            else:
                print("  No elevator data.")
    except Exception as e:
        print(f"  Error: {e}")
    return False

# PNUs
pnus = [
    ("Gangseo Sports Park", "2644010100121540000"),
    ("Shinsegae Centum", "2635010500115150000"),
    ("Lotte World Tower", "1171010100100290000"),
    ("Seoul City Hall", "1114011400100310000"), # 태평로1가 31
    ("GFC", "1168010100107370000"),
]

for label, p in pnus:
    if check_elevator(p, label):
        print(f"\nSUCCESS! Found a PNU: {p}")
        break
