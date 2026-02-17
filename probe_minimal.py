import requests
import urllib.parse

def probe_minimal():
    key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    enc_key = urllib.parse.quote(key)
    connector = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # 1. Try HTTPS for the target URL (as per screenshot)
    # 2. Try WITHOUT yadmNm to see if we get *anything* (avoid encoding issues)
    
    base_v1 = "http://apis.data.go.kr/B551182/hospInfoService1"
    base_v2 = "https://apis.data.go.kr/B551182/hospInfoServicev2" # HTTPS
    
    ops = [
        ("V1_HTTP_NoName", f"{base_v1}/getHospBasisList1^serviceKey={enc_key}|_type=json|numOfRows=1|pageNo=1"),
        ("V2_HTTPS_NoName", f"{base_v2}/getHospBasisList^serviceKey={enc_key}|_type=json|numOfRows=1|pageNo=1"),
        ("V2_HTTPS_List1_NoName", f"{base_v2}/getHospBasisList1^serviceKey={enc_key}|_type=json|numOfRows=1|pageNo=1"),
    ]
    
    # Also add one that uses URL encoding for the target URL itself (just in case the connector needs it)
    # But usually 'urllib.parse.quote' is applied to the WHOLE url param value in the request
    
    log_lines = []
    
    for label, query in ops:
        print(f"Testing {label}...")
        try:
            # We must verify logic for the connector: 
            # The connector expects ?url=... 
            # requests.get will encode the query param value automatically.
            
            res = requests.get(connector, params={'url': query}, timeout=10, verify=False)
            print(f"Status: {res.status_code}")
            print(f"Length: {len(res.text)}")
            print(f"Body: {res.text[:300]}")
            
            log_lines.append(f"[{label}] Status: {res.status_code}, Len: {len(res.text)}, Body: {res.text[:100]}")
            
        except Exception as e:
            print(f"Error: {e}")
            log_lines.append(f"[{label}] Error: {e}")
            
    with open("minimal_result.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

if __name__ == "__main__":
    probe_minimal()
