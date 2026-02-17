import requests
import urllib.parse
import json

NEW_KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
URL_V1 = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
URL_V2 = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

def confirm_key():
    results = []
    
    targets = [
        ("V1", URL_V1),
        ("V2", URL_V2)
    ]
    
    for label, url in targets:
        print(f"Checking {label}...")
        try:
            # Method 1: Auto
            res = requests.get(url, params={'serviceKey': NEW_KEY, 'pageNo': 1, 'numOfRows': 1, '_type': 'json'}, timeout=5)
            if res.status_code == 200 and 'response' in res.text:
                results.append(f"{label} [AutoParams]: SUCCESS")
            else:
                results.append(f"{label} [AutoParams]: FAILED ({res.status_code})")
                
            # Method 2: Manual ServiceKey
            qs = f"ServiceKey={NEW_KEY}&pageNo=1&numOfRows=1&_type=json"
            full_url = f"{url}?{qs}"
            res = requests.get(full_url, timeout=5)
            if res.status_code == 200 and 'response' in res.text:
                 results.append(f"{label} [ManualKey]: SUCCESS")
            else:
                 results.append(f"{label} [ManualKey]: FAILED ({res.status_code})")
                 
        except Exception as e:
            results.append(f"{label}: ERROR {e}")
            
    with open("key_confirm_result.txt", "w") as f:
        f.write("\n".join(results))
        
    print("Done. Check key_confirm_result.txt")

if __name__ == "__main__":
    confirm_key()
