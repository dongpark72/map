
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def debug_seoul():
    # Seoul Jongno-gu Gyeonji-dong 68-5
    sigungu = "11110"
    # Gyeonji-dong code guess... 
    # Let's try iterating common Jongno codes or search
    # According to public data, Gyeonji-dong might be 13300.
    
    auth_key = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
    enc_key = urllib.parse.quote(auth_key)
    base_url = "http://apis.data.go.kr/1613000/BldRgstHubService"
    
    possible_dongs = ["12900"]
    
    found_pk = None

    for dong in possible_dongs:
        print(f"Checking Dong: {dong} ...")
        url_title = f"{base_url}/getBrTitleInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={dong}&platGbCd=0&bun=0068&ji=0005"
        try:
            res = requests.get(url_title, timeout=5)
            if "<item>" in res.text:
                print(f"FOUND Title in {dong}!")
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                for it in items:
                    pk = it.find('mgmBldrgstPk').text
                    nm = it.find('bldNm').text
                    print(f"  Building: {nm}, PK: {pk}")
                    found_pk = pk
                break
        except Exception as e:
            print(e)
            
    if not found_pk:
        print("Could not find building PK.")
        return

    # Check Floor Info
    print(f"\n--- Checking Floor Info (getBrFlrOulnInfo) for PK {found_pk} ---")
    url_flr = f"{base_url}/getBrFlrOulnInfo?serviceKey={enc_key}&numOfRows=100&pageNo=1&mgmBldrgstPk={found_pk}"
    res_flr = requests.get(url_flr, timeout=5)
    print(f"Status: {res_flr.status_code}")
    print(res_flr.text) # Print FULL XML
    if "<item>" in res_flr.text:
        print("Floor Info FOUND.")
    else:
        print("Floor Info EMPTY.")

    # Check Exclusive Area
    print(f"\n--- Checking Exclusive Area (getBrExposPubuseAreaInfo) for PK {found_pk} ---")
    url_ex = f"{base_url}/getBrExposPubuseAreaInfo?serviceKey={enc_key}&numOfRows=100&pageNo=1&mgmBldrgstPk={found_pk}"
    res_ex = requests.get(url_ex, timeout=5)
    print(f"Status: {res_ex.status_code}")
    if "<item>" in res_ex.text:
        print("Exclusive Area FOUND.")
        print(res_ex.text[:300])
    else:
        print("Exclusive Area EMPTY.")


if __name__ == "__main__":
    debug_seoul()
