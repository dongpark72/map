import requests
import urllib.parse
import json

def check_v2_endpoint():
    key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    enc_key = urllib.parse.quote(key)
    connector = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # User's approved endpoint base
    base_v2 = "http://apis.data.go.kr/B551182/hospInfoServicev2"
    
    # Variations to try
    variations = [
        "getHospBasisList",
        "getHospBasisList1",
        "getHospBasisList2" # Often v2 uses 2
    ]
    
    target_name = "서울특별시서울의료원"
    enc_name = urllib.parse.quote(target_name)
    
    print(f"--- Probing V2 Endpoints for {target_name} ---")
    
    for op in variations:
        url = f"{base_v2}/{op}"
        print(f"\n[Testing {op}]")
        query = f"{url}^serviceKey={enc_key}|_type=json|yadmNm={enc_name}|numOfRows=1|pageNo=1"
        
        try:
            res = requests.get(connector, params={'url': query}, timeout=10, verify=False)
            print(f"Status: {res.status_code}")
            sample = res.text[:300]
            print(f"Body: {sample}")
            
            if '"header"' in res.text or '<header>' in res.text:
                if '"resultCode":"00"' in res.text or '<resultCode>00</resultCode>' in res.text:
                    print(f"!!! SUCCESS with {op} !!!")
                    break
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_v2_endpoint()
