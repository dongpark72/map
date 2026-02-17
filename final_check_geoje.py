
import requests
import xml.etree.ElementTree as ET
import urllib.parse
import json

def final_check():
    # Target: Gyeongsangnam-do Geoje-si Jangseungpo-dong 101-8
    pnu_target = "4831010200101010008" 
    
    # Control: Busan Haeundae-gu U-dong 1408 (Marine City I-Park - likely to have data)
    # PNU: 2635010500114080000 
    pnu_control = "2635010500114080000"

    print(f"checking Target PNU: {pnu_target}...")
    check_pnu(pnu_target, "TARGET (Geoje)")
    
    print(f"\nchecking Control PNU: {pnu_control} (Busan Marine City) for verification...")
    check_pnu(pnu_control, "CONTROL (Marine City)")

def check_pnu(pnu, label):
    # Keys
    keys = [
        "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368",
        "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    ]
    base_url = "http://apis.data.go.kr/1613000/BldRgstHubService"
    
    # 1. Check Title to get PK (We need PK for Floor API)
    # But usually parsing PNU for params is standard.
    sigungu = pnu[0:5]
    bjdong = pnu[5:10]
    platGb = '0' if pnu[10] == '1' else '1'
    bun = pnu[11:15]
    ji = pnu[15:19]

    main_pk = None
    
    for key in keys:
        enc_key = urllib.parse.quote(key)
        
        # Get Title
        try:
            url_t = f"{base_url}/getBrTitleInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
            res = requests.get(url_t, timeout=5)
            if "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                # Pick the largest building
                max_area = 0
                for it in items:
                    pk = it.find('mgmBldrgstPk').text
                    a = float(it.find('totArea').text or 0)
                    if a > max_area:
                        max_area = a
                        main_pk = pk
                if main_pk: break
        except: pass
    
    if not main_pk:
        print(f" [{label}] No Building Title found (Cannot check floors without PK).")
        return

    print(f" [{label}] Found Main PK: {main_pk}")

    # 2. Check Floors (FlrOuln)
    found_floor = False
    for key in keys:
        enc_key = urllib.parse.quote(key)
        try:
            url = f"{base_url}/getBrFlrOulnInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&mgmBldrgstPk={main_pk}"
            res = requests.get(url, timeout=5)
            cnt = res.text.count('<item>')
            if cnt > 0:
                print(f" [{label}] Floor Info: FOUND {cnt} items.")
                found_floor = True
                break
        except: pass
    
    if found_floor: print(f" [{label}] Floor: FOUND.")
    else: print(f" [{label}] Floor: NONE.")

    # 3. Check Expos
    found_expos = False
    for key in keys:
        enc_key = urllib.parse.quote(key)
        try:
            url = f"{base_url}/getBrExposPubuseAreaInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&mgmBldrgstPk={main_pk}"
            res = requests.get(url, timeout=5)
            cnt = res.text.count('<item>')
            if cnt > 0:
                print(f" [{label}] Expos Info: FOUND {cnt} items.")
                found_expos = True
                break
        except: pass

    if found_expos: print(f" [{label}] Expos: FOUND.")
    else: print(f" [{label}] Expos: NONE.")
        
    # 4. V-World check
    vw_key = "F78E51BE-4005-3AFF-91E0-BDDBAC8478D0"
    params = {
        "service": "data", "request": "GetFeature", "data": "LT_C_SPBD",
        "key": vw_key, "format": "json", "attrFilter": f"pnu:like:{pnu}", "domain": "http://localhost"
    }
    try:
        res_v = requests.get("https://api.vworld.kr/req/data", params=params, timeout=5)
        feats = res_v.json().get('response', {}).get('result', {}).get('featureCollection', {}).get('features', [])
        print(f" [{label}] V-World: {len(feats)}")
    except:
        print(f" [{label}] V-World: Err")

if __name__ == "__main__":
    final_check()
