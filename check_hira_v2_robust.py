import requests
import urllib.parse
import json
import traceback

def check_v2_robust():
    log_lines = []
    def log(msg):
        print(msg)
        log_lines.append(str(msg))

    key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    enc_key = urllib.parse.quote(key)
    connector = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # User's approved endpoint base
    base_v2 = "http://apis.data.go.kr/B551182/hospInfoServicev2"
    
    variations = [
        "getHospBasisList",
        "getHospBasisList1", 
        "getHospBasisList2" 
    ]
    
    target_name = "서울특별시서울의료원"
    enc_name = urllib.parse.quote(target_name)
    
    log(f"--- Probing V2 Endpoints for {target_name} ---")
    
    for op in variations:
        url = f"{base_v2}/{op}"
        log(f"\n[Testing {op}]")
        query = f"{url}^serviceKey={enc_key}|_type=json|yadmNm={enc_name}|numOfRows=1|pageNo=1"
        
        try:
            res = requests.get(connector, params={'url': query}, timeout=10, verify=False)
            log(f"Status: {res.status_code}")
            
            # Check content length and body
            log(f"Length: {len(res.text)}")
            log(f"Body: {res.text[:500]}")
            
            if '"header"' in res.text or '<header>' in res.text:
                if '"resultCode":"00"' in res.text or '<resultCode>00</resultCode>' in res.text:
                    log(f"!!! SUCCESS with {op} !!!")
        except Exception as e:
            log(f"Error: {e}")

    with open("v2_result.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

if __name__ == "__main__":
    check_v2_robust()
