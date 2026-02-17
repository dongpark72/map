import requests
import urllib.parse
import xml.etree.ElementTree as ET

API_KEY = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
api_url_elvt = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrElvtInfo"

def check_building_and_elevator(pnu):
    sigunguCd = pnu[0:5]
    bjdongCd = pnu[5:10]
    platGbCd = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15]))
    ji = str(int(pnu[15:19]))
    
    enc_key = urllib.parse.quote(API_KEY)
    
    print(f"\n--- Checking PNU: {pnu} ---")
    
    # 1. Title Info
    q_title = f"{api_url_title}^serviceKey={enc_key}|numOfRows=10|pageNo=1|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={platGbCd}|bun={bun}|ji={ji}"
    try:
        res = requests.get(connector_url, params={'url': q_title}, timeout=10)
        if res.status_code == 200:
            if "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                print(f"  Title: Found {len(items)} buildings.")
                for item in items[:2]:
                    print(f"    - {item.findtext('bldNm', 'N/A')} ({item.findtext('dongNm', 'N/A')})")
            else:
                print("  Title: No building found. (Maybe PNU error)")
                return False
        else:
            print(f"  Title: API Error {res.status_code}")
            return False
    except Exception as e:
        print(f"  Title: Error {e}")
        return False

    # 2. Elevator Info
    q_elvt = f"{api_url_elvt}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={platGbCd}|bun={bun}|ji={ji}"
    try:
        res = requests.get(connector_url, params={'url': q_elvt}, timeout=10)
        if res.status_code == 200:
            if "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                print(f"  Elevator: SUCCESS! Found {len(items)} records.")
                for item in items:
                    dong = item.findtext('dongNm', 'N/A')
                    gb = item.findtext('elvtGbCdNm', 'N/A')
                    cnt = item.findtext('elvtCnt', '0')
                    print(f"    - Dong: {dong}, Type: {gb}, Count: {cnt}")
                return True
            else:
                print("  Elevator: No elevator data found.")
    except Exception as e:
        print(f"  Elevator: Error {e}")
    
    return False

# PNU list
pnus = [
    "1165010700100200043", # 반포자이 (Banpo Xi)
    "1165010800100180001", # 반포동 래미안퍼스티지
    "1168010600105110000", # 대치동 은마아파트
    "2635010500114670000", # 우동 마린시티 아이파크?
    "1174010900104300000", # 천호동 (Old high rise?)
]

for p in pnus:
    if check_building_and_elevator(p):
        print(f"\nFINAL DISCOVERY PNU: {p}")
        break
