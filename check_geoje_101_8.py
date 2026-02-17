
import requests
import xml.etree.ElementTree as ET
import urllib.parse
import json

def check_geoje():
    # Address: Gyeongsangnam-do Geoje-si Jangseungpo-dong 101-8
    # PNU: 4831010200101010008
    sigungu = "48310"
    bjdong = "10200"
    platGb = "0"
    bun = "0101"
    ji = "0008"
    pnu = "4831010200101010008"
    
    # ---------------------------------------------------------
    # 1. Public Data Portal Check
    # ---------------------------------------------------------
    print("=== 1. Public Data Portal Check ===")
    auth_key = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
    enc_key = urllib.parse.quote(auth_key)
    base_url = "http://apis.data.go.kr/1613000/BldRgstHubService"
    
    main_pk = None
    
    # 1-1. Title Info
    print(" [Title Info]")
    url_title = f"{base_url}/getBrTitleInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
    try:
        res = requests.get(url_title, timeout=5)
        if "<item>" in res.text:
            items = ET.fromstring(res.text).findall('.//item')
            print(f" [Title] Found: {len(items)} bldgs.")
            for it in items:
                print(f"  > {it.find('bldNm').text} (Area: {it.find('totArea').text})")
                pk = it.find('mgmBldrgstPk').text
                if not main_pk: main_pk = pk
        else:
            print(" [Title] Found: 0 bldgs.")
    except Exception as e: print(f"Title Error: {e}")

    if main_pk:
        # 1-2. Floor Info
        try:
            res_f = requests.get(f"{base_url}/getBrFlrOulnInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&mgmBldrgstPk={main_pk}", timeout=5)
            cnt_f = res_f.text.count('<item>')
            print(f" [Floor] Records: {cnt_f}")
        except: print(" [Floor] Error")

        # 1-3. Expos Info
        try:
            res_x = requests.get(f"{base_url}/getBrExposPubuseAreaInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&mgmBldrgstPk={main_pk}", timeout=5)
            cnt_x = res_x.text.count('<item>')
            print(f" [Expos] Records: {cnt_x}")
        except: print(" [Expos] Error")
            
    # 2. V-World Check
    print("=== 2. V-World Check ===")
    vw_key = "F78E51BE-4005-3AFF-91E0-BDDBAC8478D0"
    vw_url = "https://api.vworld.kr/req/data"
    params = {
        "service": "data",
        "request": "GetFeature",
        "data": "LT_C_SPBD",
        "key": vw_key,
        "format": "json",
        "attrFilter": f"pnu:like:{pnu}",
        "domain": "http://localhost:8000"
    }

    try:
        res_v = requests.get(vw_url, params=params, timeout=10)
        feats = res_v.json().get('response', {}).get('result', {}).get('featureCollection', {}).get('features', [])
        print(f" [V-World] Polygons: {len(feats)}")
    except: print(" [V-World] Error")

if __name__ == "__main__":
    check_geoje()
