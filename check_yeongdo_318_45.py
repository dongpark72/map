
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def check_yeongdo():
    # Busan Yeongdo-gu Dongsam-dong 318-45
    sigungu = "26200"
    bjdong = "10300"
    platGb = "0"
    bun = "0318"
    ji = "0045"
    base_url = "http://apis.data.go.kr/1613000/BldRgstHubService"
    
    # Try both keys
    keys = [
        "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368",
        "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    ]
    
    main_pk = None

    for k in keys:
        if main_pk: break
        enc_key = urllib.parse.quote(k)
        print(f"--- Trying Key: {k[:10]}... ---")

        # 0. Check Recap
        print(" [Recap]")
        url_recap = f"{base_url}/getBrRecapTitleInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
        try:
            res = requests.get(url_recap, timeout=5)
            if "<item>" in res.text:
                print(" FOUND IN RECAP!")
                # Extract PK from Recap? Recap might usually have PK.
                # But typically we rely on Title for PK list.
                # Let's check keys in Recap items.
                root = ET.fromstring(res.text)
                for it in root.findall('.//item'):
                    pk = it.find('mgmBldrgstPk').text
                    print(f"  Recap PK: {pk}")
                    main_pk = pk
                    break
        except: pass

        if main_pk: break

        # 1. Get Title Info
        print(" [Title]")
        url_title = f"{base_url}/getBrTitleInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
        try:
            res = requests.get(url_title, timeout=5)
            print(f"Title Status: {res.status_code}")
            root = ET.fromstring(res.text)
            items = root.findall('.//item')
            print(f"Found {len(items)} buildings.")
            
            # Find main building (largest area)
            max_area = 0
            for item in items:
                pk = item.find('mgmBldrgstPk').text
                nm = item.find('bldNm').text
                dong = item.find('dongNm').text if item.find('dongNm') is not None else ""
                area = float(item.find('totArea').text)
                print(f" - {nm} {dong} (PK: {pk}, Area: {area})")
                
                if area > max_area:
                    max_area = area
                    main_pk = pk
                
        except Exception as e:
            print(f"Title Error: {e}")
            continue

    if not main_pk:
        print("No main building found in Title/Recap.")
        # Try checking Expos directly by PNU (Just to see if data exists)
        print("--- 3. Checking Expos DIRECTLY by PNU ---")
        url_ex_pnu = f"{base_url}/getBrExposPubuseAreaInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
        try:
             res_x = requests.get(url_ex_pnu, timeout=5)
             if "<item>" in res_x.text:
                 print(" FOUND IN EXPOS (PNU Search)!")
                 items = ET.fromstring(res_x.text).findall('.//item')
                 for it in items:
                     print(f"  Expos: {it.find('dongNm').text} - {it.find('flrNoNm').text}")
             else:
                 print(" Not found in Expos (PNU Search) either.")
        except Exception as e:
            print(f"Expos PNU Error: {e}")
        return

    print(f"\nTargeting PK: {main_pk}")

    # 2. Check Floor Info (getBrFlrOulnInfo)
    print("--- 2. Checking Floor Info (FlrOuln) ---")
    url_flr = f"{base_url}/getBrFlrOulnInfo?serviceKey={enc_key}&numOfRows=999&pageNo=1&mgmBldrgstPk={main_pk}"
    try:
        res_f = requests.get(url_flr, timeout=5)
        if "<item>" in res_f.text:
            items_f = ET.fromstring(res_f.text).findall('.//item')
            print(f"SUCCESS: Found {len(items_f)} floor records.")
            for i, f in enumerate(items_f[:3]): # First 3 only
                print(f"  {i+1}. {f.find('flrNoNm').text} - {f.find('mainPurpsCdNm').text}")
        else:
            print("FAILED: No floor data found.")
    except Exception as e:
        print(f"Floor Error: {e}")

    # 3. Check Exclusive Info (getBrExposPubuseAreaInfo)
    print("\n--- 3. Checking Exclusive Info (Expos) ---")
    url_ex = f"{base_url}/getBrExposPubuseAreaInfo?serviceKey={enc_key}&numOfRows=999&pageNo=1&mgmBldrgstPk={main_pk}"
    try:
        res_x = requests.get(url_ex, timeout=5)
        if "<item>" in res_x.text:
            items_x = ET.fromstring(res_x.text).findall('.//item')
            print(f"SUCCESS: Found {len(items_x)} exclusive records.")
            for i, x in enumerate(items_x[:3]):
                print(f"  {i+1}. {x.find('flrNoNm').text} - {x.find('mainPurpsCdNm').text}")
        else:
             print("FAILED: No exclusive data found.")

    except Exception as e:
        print(f"Expos Error: {e}")

if __name__ == "__main__":
    check_yeongdo()
