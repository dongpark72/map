
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def check(sigungu, bjdong, platGb, bun, ji, enc_key, base_url):
    # Try Recap first to see if PNU is valid
    print(f"--- Fetching Recap Info for {bun}-{ji} ---")
    url_recap = f"{base_url}/getBrRecapTitleInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
    
    try:
        res_re = requests.get(url_recap, timeout=10)
        print(f"Recap Status: {res_re.status_code}")
        if "<item>" in res_re.text:
            print("Recap Found!")
            # print(res_re.text[:300])
        else:
            print("Recap Not Found.")
    except Exception as e:
        print(f"Recap Error: {e}")

    print(f"--- Fecthing Title Info for {bun}-{ji} ---")
    url_title = f"{base_url}/getBrTitleInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
    print(f"Title URL: {url_title}")
    
    try:
        res = requests.get(url_title, timeout=10)
        print(f"Title Status: {res.status_code}")
        
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        print(f"Found {len(items)} buildings.")
        
        main_pk = None
        main_bld_nm = ""
        max_area = 0.0
        
        for item in items:
            pk = item.find('mgmBldrgstPk').text
            nm = item.find('bldNm').text
            area = float(item.find('totArea').text)
            print(f" - {nm} (PK: {pk}, Area: {area})")
            
            if area > max_area:
                max_area = area
                main_pk = pk
                main_bld_nm = nm
        
        if not main_pk:
            print("No main building found.")
            return

        print(f"Targeting Main Building: {main_bld_nm} (PK: {main_pk})")
        
        # 2. Get Floor Info (getBrFlrOulnInfo)
        print(f"--- Fetching Floor Info (getBrFlrOulnInfo) ---")
        url_flr = f"{base_url}/getBrFlrOulnInfo?serviceKey={enc_key}&numOfRows=100&pageNo=1&mgmBldrgstPk={main_pk}"
        res_flr = requests.get(url_flr, timeout=10)
        print(f"Floor Status: {res_flr.status_code}")
        f_count = 0
        if "<item>" in res_flr.text:
            f_items = ET.fromstring(res_flr.text).findall('.//item')
            f_count = len(f_items)
            print(f"Found {f_count} floor records.")
            for f in f_items:
                flr_no = f.find('flrNo').text
                flr_nm = f.find('flrNoNm').text
                print(f"  > {flr_no}F ({flr_nm})")
        else:
            print("No floor data found in getBrFlrOulnInfo.")

        # 3. Get Exclusive Area Info (getBrExposPubuseAreaInfo)
        if f_count == 0:
            print(f"--- Fetching Exclusive Area (getBrExposPubuseAreaInfo) ---")
            url_expos = f"{base_url}/getBrExposPubuseAreaInfo?serviceKey={enc_key}&numOfRows=100&pageNo=1&mgmBldrgstPk={main_pk}"
            res_expos = requests.get(url_expos, timeout=10)
            print(f"Expos Status: {res_expos.status_code}")
            if "<item>" in res_expos.text:
                x_items = ET.fromstring(res_expos.text).findall('.//item')
                print(f"Found {len(x_items)} exclusive area records.")
                for x in x_items:
                    flr = x.find('flrNo').text
                    print(f"  > {flr}F")
            else:
                 print("No data in getBrExposPubuseAreaInfo.")

    except Exception as e:
        print(f"Error: {e}")

def debug_floor_info():
    sigungu = "26200"
    platGb = "0"
    
    auth_key = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
    enc_key = urllib.parse.quote(auth_key)
    base_url = "http://apis.data.go.kr/1613000/BldRgstHubService"
    
    # Try various bjdong codes
    for dong in ["10300", "12100", "10100", "10200", "10400", "10500"]:
        print(f"\nScanning Dong Code: {dong} ...")
        # Try both bun-ji
        # 318-45
        if check_pnu(sigungu, dong, platGb, "0318", "0045", enc_key, base_url):
            print(f"FOUND MATCH at {dong}-0318-0045")
            check(sigungu, dong, platGb, "0318", "0045", enc_key, base_url)
            break
        
        # 318-49 (Just in case)
        if check_pnu(sigungu, dong, platGb, "0318", "0049", enc_key, base_url):
            print(f"FOUND MATCH at {dong}-0318-0049")
            check(sigungu, dong, platGb, "0318", "0049", enc_key, base_url)
            break

def check_pnu(sigungu, bjdong, platGb, bun, ji, enc_key, base_url):
    url = f"{base_url}/getBrTitleInfo?serviceKey={enc_key}&numOfRows=1&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
    try:
        res = requests.get(url, timeout=5)
        return "<item>" in res.text
    except:
        return False


if __name__ == "__main__":
    debug_floor_info()
