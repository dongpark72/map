
import requests
import xml.etree.ElementTree as ET
import urllib.parse
import logging

# Mock logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_building_proxy():
    pnu = "1111013800101550002" # Seoul Jongno-gu Gwanhun-dong 155-2
    # pnu = "2644010400..." # One typically used in tests? But let's use the one from the screenshot.
    
    pnus_to_try = [pnu]
    # No alt pnu logic needed for Seoul usually, but keeping structure
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    api_url_recap = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
    api_url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
    api_url_flr = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
    api_url_pkng = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrPkngInfo"
    api_url_eler = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrElerInfo"
    
    # Try the user suggested ones too if these stick
    # api_url_pkng = "http://apis.data.go.kr/1613000/BldRgstHubService/getBundangPkngInfo" 
    # api_url_eler = "http://apis.data.go.kr/1613000/BldRgstHubService/getBundangElerInfo"

    keys_to_try = [
        "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
        "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368",
    ]
    
    result_data = {'title': {}, 'floors': []}
    
    working_key = keys_to_try[0]
    site_pks = set()
    all_candidate_items = []
    
    print("Step 1: Fetching Title Info...")
    for target_pnu in pnus_to_try:
        sigungu = target_pnu[0:5]
        bjdong = target_pnu[5:10]
        platGb = '0' if target_pnu[10] == '1' else '1'
        bun = str(int(target_pnu[11:15])).zfill(4)
        ji = str(int(target_pnu[15:19])).zfill(4)
        
        print(f"Target: {sigungu} {bjdong} {platGb} {bun} {ji}")

        for key in keys_to_try:
            enc_key = urllib.parse.quote(key)
            found = False
            for base_url in [api_url_recap, api_url_title]:
                try:
                    q = f"{base_url}^serviceKey={enc_key}|numOfRows=100|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
                    print(f"Requesting: {base_url}...")
                    res = session.get(connector_url, params={'url': q}, timeout=10)
                    print(f"Status: {res.status_code}")
                    if res.status_code == 200:
                        # Check if response is error xml
                        if '<errMsg>' in res.text:
                            print("Error in response:", res.text[:200])
                            continue
                            
                        items = ET.fromstring(res.text).findall('.//item')
                        if items:
                            print(f"Found {len(items)} items")
                            all_candidate_items.extend(items)
                            for it in items:
                                pk = it.find('mgmBldrgstPk').text if it.find('mgmBldrgstPk') is not None else None
                                if pk: site_pks.add(pk)
                            found = True
                        else:
                            print("No items found.")
                except Exception as e:
                    print(f"Error: {e}")
            
            if found:
                working_key = key
                print("Found working key.")
                break
        if site_pks: break
        
    print(f"Total Candidate Items: {len(all_candidate_items)}")
    print(f"Site PKs: {site_pks}")

    if not all_candidate_items:
        print("No items found, exiting.")
        return

    def gn(it, tag):
        v = it.find(tag).text if it.find(tag) is not None and it.find(tag).text else '0'
        try: return float("".join(filter(lambda x: x.isdigit() or x=='.', v)))
        except: return 0

    main_item = max(all_candidate_items, key=lambda x: gn(x, 'totArea'))
    print(f"Main Item: {main_item.find('bldNm').text if main_item.find('bldNm') is not None else 'Unknown'}")

    enc_key = urllib.parse.quote(working_key)
    
    total_p_auto = 0
    total_p_mech = 0
    total_e_ride = 0
    total_e_emgen = 0
    
    print("Step 2: Fetching Parking/Elevator details...")
    for pk in site_pks:
        print(f"Checking PK: {pk}")
        # Pkng
        try:
            q_p = f"{api_url_pkng}^serviceKey={enc_key}|numOfRows=100|mgmBldrgstPk={pk}"
            res_p = session.get(connector_url, params={'url': q_p}, timeout=5)
            if res_p.status_code == 200:
                p_items = ET.fromstring(res_p.text).findall('.//item')
                print(f"  Pkng Items: {len(p_items)}")
                for p_it in p_items:
                    def gv(tag):
                        v = p_it.find(tag).text if p_it.find(tag) is not None and p_it.find(tag).text else '0'
                        try: return int(float(v))
                        except: return 0
                    total_p_auto += gv('indrAutoUtCnt') + gv('oudrAutoUtCnt')
                    total_p_mech += gv('indrMechUtCnt') + gv('oudrMechUtCnt')
        except Exception as e: print(e)

        # Eler
        try:
            q_e = f"{api_url_eler}^serviceKey={enc_key}|numOfRows=100|mgmBldrgstPk={pk}"
            res_e = session.get(connector_url, params={'url': q_e}, timeout=5)
            if res_e.status_code == 200:
                e_items = ET.fromstring(res_e.text).findall('.//item')
                print(f"  Eler Items: {len(e_items)}")
                for e_it in e_items:
                    def gv(tag):
                        v = e_it.find(tag).text if e_it.find(tag) is not None and e_it.find(tag).text else '0'
                        try: return int(float(v))
                        except: return 0
                    gb = e_it.find('elerGbCdNm').text if e_it.find('elerGbCdNm') is not None else ''
                    if '비상' in gb: total_e_emgen += gv('elerCnt')
                    else: total_e_ride += gv('elerCnt')
        except Exception as e: print(e)
            
    print(f"Total Parking: Auto={total_p_auto}, Mech={total_p_mech}")
    print(f"Total Elevator: Ride={total_e_ride}, Emgen={total_e_emgen}")

if __name__ == "__main__":
    test_building_proxy()
