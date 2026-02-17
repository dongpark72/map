import requests
import urllib.parse
import xml.etree.ElementTree as ET

API_KEY = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url_elvt = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrElvtInfo"

def parse_pnu(pnu):
    return {
        'sigunguCd': pnu[0:5],
        'bjdongCd': pnu[5:10],
        'platGbCd': '0' if pnu[10] == '1' else '1',
        'bun': str(int(pnu[11:15])),
        'ji': str(int(pnu[15:19]))
    }

def check_elevator(pnu):
    params = parse_pnu(pnu)
    enc_key = urllib.parse.quote(API_KEY)
    q_elvt = f"{api_url_elvt}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={params['sigunguCd']}|bjdongCd={params['bjdongCd']}|platGbCd={params['platGbCd']}|bun={params['bun']}|ji={params['ji']}"
    
    print(f"Testing PNU: {pnu} (bun={params['bun']}, ji={params['ji']})")
    try:
        res = requests.get(connector_url, params={'url': q_elvt}, timeout=10)
        if res.status_code == 200:
            if "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                if items:
                    print(f"  Found {len(items)} elevator records.")
                    for item in items:
                        dong = item.findtext('dongNm', 'N/A')
                        gb = item.findtext('elvtGbCdNm', 'N/A')
                        cnt = item.findtext('elvtCnt', '0')
                        print(f"    - Dong: {dong}, Type: {gb}, Count: {cnt}")
                    return True
                else:
                    print("  <item> tags found but no actual records?")
            else:
                print("  No elevator data found (no <item> in response).")
        else:
            print(f"  API Error: {res.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    return False

# PNUs for buildings that CERTAINLY have elevators
pnus = [
    "1111011600100990000", # 서린동 99 (SK Building)
    "1114011400101200000", # 태평로2가 120 (Samsung Main Building)
    "1165010100113200010", # 서초동 1320-10 (GT Tower)
    "1168010100107370000", # 역삼동 737 (GFC)
    "1111011900100330000", # 세종로 33 (Kyobo Building) - Wait, Sejongno 33 or 1?
    "1171010100100070018", # Jamsil Lotte Castle?
    "2620010300103180049" # From the project, maybe 11th digit should be checked
]

for p in pnus:
    if check_elevator(p):
        print(f"\nSUCCESS! Found a PNU with elevator info: {p}")
        break
