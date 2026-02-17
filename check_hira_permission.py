import requests
import urllib.parse
import json
import traceback

def check_permission():
    result_log = []
    
    def log(msg):
        print(msg)
        result_log.append(str(msg))

    try:
        # API Keys
        key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368' # The one from user screen
        enc_key = urllib.parse.quote(key)
        
        # Connector URL
        connector = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
        
        # Step 1: Basis Info
        basis_url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
        hos_name = "동탄아이엠유의원"
        
        log(f"--- STEP 1: Basis Info for {hos_name} ---")
        q1 = f"{basis_url}^serviceKey={enc_key}|_type=json|yadmNm={hos_name}|numOfRows=1|pageNo=1"
        
        res1 = requests.get(connector, params={'url': q1}, timeout=15, verify=False)
        log(f"Status: {res1.status_code}")
        log(f"Headers: {res1.headers}")
        log(f"Body First 500: {res1.text[:500]}")
        
        ykiho = None
        
        # Try JSON parse
        try:
            d1 = res1.json()
            items = d1.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            if isinstance(items, list) and items:
                ykiho = items[0].get('ykiho')
            elif isinstance(items, dict):
                ykiho = items.get('ykiho')
        except:
            log("JSON parse failed, checking XML string manually")
            if '<ykiho>' in res1.text:
                import re
                m = re.search(r'<ykiho>(.*?)</ykiho>', res1.text)
                if m: ykiho = m.group(1)
        
        log(f"Found ykiho: {ykiho}")
        
        if not ykiho:
            log("STOP: Could not get ykiho. Check 'Hospital Information Service' permission.")
        else:
            # Step 2: Detail Info
            log(f"\n--- STEP 2: Detail Info for {ykiho} ---")
            detail_url = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7"
            q2 = f"{detail_url}^serviceKey={enc_key}|_type=json|ykiho={ykiho}|numOfRows=1|pageNo=1"
            
            res2 = requests.get(connector, params={'url': q2}, timeout=15, verify=False)
            log(f"Status: {res2.status_code}")
            log(f"Body First 1000: {res2.text[:1000]}")
            
            if '<resultCode>00</resultCode>' in res2.text or '"resultCode":"00"' in res2.text:
                log("SUCCESS: Detail API call succeeded.")
            else:
                log("FAILURE: Detail API call returned non-success code. Likely permission issue.")
                
    except Exception as e:
        log(f"EXCEPTION: {traceback.format_exc()}")

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(result_log))

if __name__ == "__main__":
    check_permission()
