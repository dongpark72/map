import requests
import urllib.parse
import xml.etree.ElementTree as ET

API_KEY = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url_elvt = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrElvtInfo"

def check_elevator(pnu):
    sigunguCd = pnu[0:5]
    bjdongCd = pnu[5:10]
    platGbCd = pnu[10] # Using 0 directly if it starts with 1
    if platGbCd == '1': platGbCd = '0'
    elif platGbCd == '2': platGbCd = '1'
    
    bun = str(int(pnu[11:15]))
    ji = str(int(pnu[15:19]))
    
    enc_key = urllib.parse.quote(API_KEY)
    q_elvt = f"{api_url_elvt}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={platGbCd}|bun={bun}|ji={ji}"
    
    print(f"Testing PNU: {pnu}")
    try:
        res = requests.get(connector_url, params={'url': q_elvt}, timeout=10)
        if res.status_code == 200:
            if "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                print(f"  Found {len(items)} elevator records.")
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

# List of PNUs to check
pnus = [
    "1165010100113080026", # 서초동 1308-26 (Commercial building)
    "1168010300100120000", # 개포동
    "1168011800104670000", # 도곡동 (Tower Palace area?)
    "2620010300103180049", # 동삼동
    "1171010100100290000", # 신천동 29 (Lotte World Tower)
]

for p in pnus:
    if check_elevator(p):
        print(f"\nSUCCESS! Found a PNU with elevator info: {p}")
        break
