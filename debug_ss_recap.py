
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def debug_ss():
    # S&S Building: Jongno-gu Gyeonji-dong 68-5 (11110 12900)
    sigungu = "11110"
    bjdong = "12900"
    platGb = "0"
    bun = "0068"
    ji = "0005"
    
    auth_key = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
    enc_key = urllib.parse.quote(auth_key)
    base_url = "http://apis.data.go.kr/1613000/BldRgstHubService"
    
    # 1. Check Recap
    print("--- 1. Recap Info ---")
    url_recap = f"{base_url}/getBrRecapTitleInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
    try:
        res = requests.get(url_recap, timeout=5)
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        print(f"Recap Items: {len(items)}")
        for it in items:
            pk = it.find('mgmBldrgstPk').text
            nm = it.find('bldNm').text
            print(f" Recap PK: {pk}, Name: {nm}")
            # Try Floor on Recap PK?
            check_floor(pk, "Recap PK", enc_key, base_url)
    except Exception as e:
        print(f"Recap Error: {e}")

    # 2. Check Title
    print("\n--- 2. Title Info ---")
    url_title = f"{base_url}/getBrTitleInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}"
    try:
        res = requests.get(url_title, timeout=5)
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        print(f"Title Items: {len(items)}")
        for it in items:
            pk = it.find('mgmBldrgstPk').text
            nm = it.find('bldNm').text
            dong = it.find('dongNm').text
            print(f" Title PK: {pk}, Name: {nm}, Dong: {dong}")
            check_floor(pk, "Title PK", enc_key, base_url)
    except Exception as e:
        print(f"Title Error: {e}")

def check_floor(pk, label, enc_key, base_url):
    # FlrOuln
    url = f"{base_url}/getBrFlrOulnInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&mgmBldrgstPk={pk}"
    res = requests.get(url, timeout=5)
    cnt = res.text.count('<item>')
    print(f"  [{label}] FlrOuln Count: {cnt}")
    
    # Expos
    url2 = f"{base_url}/getBrExposPubuseAreaInfo?serviceKey={enc_key}&numOfRows=10&pageNo=1&mgmBldrgstPk={pk}"
    res2 = requests.get(url2, timeout=5)
    cnt2 = res2.text.count('<item>')
    print(f"  [{label}] Expos Count: {cnt2}")

if __name__ == "__main__":
    debug_ss()
