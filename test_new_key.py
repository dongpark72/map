import requests
import urllib.parse
import json

# User provided new key
NEW_KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

# Endpoints to test
URL_V1 = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
URL_V2 = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

def test_new_key():
    print(f"Testing with Key: {NEW_KEY}")
    
    # Since the key is Hex-like, it might not need URL encoding, but let's try both.
    # Actually, if it's a Hex string, urllib.parse.quote(key) is just the key itself 
    # (unless it has special chars, which hex doesn't).
    
    encoded_key = urllib.parse.quote(NEW_KEY) # Should be same as NEW_KEY if pure hex
    
    targets = [
        ("V1", URL_V1),
        ("V2", URL_V2)
    ]
    
    for label, url in targets:
        print(f"\n--- Testing {label} : {url} ---")
        
        # Method 1: requests params (Automatic)
        try:
            params = {
                'serviceKey': NEW_KEY,
                'pageNo': '1',
                'numOfRows': '1',
                '_type': 'json'
            }
            res = requests.get(url, params=params, timeout=5)
            print(f"[Method 1 - Auto Params] Status: {res.status_code}")
            if res.status_code == 200:
                print(f"Body: {res.text[:300]}")
            else:
                print(f"Body: {res.text[:100]}")
                
        except Exception as e:
            print(f"[Method 1] Error: {e}")

        # Method 2: Manual Query String (ServiceKey=...)
        # Sometimes 'ServiceKey' (capital S) is required
        try:
            qs = f"ServiceKey={NEW_KEY}&pageNo=1&numOfRows=1&_type=json"
            full_url = f"{url}?{qs}"
            res = requests.get(full_url, timeout=5)
            print(f"[Method 2 - Manual ServiceKey] Status: {res.status_code}")
            if res.status_code == 200:
                print(f"Body: {res.text[:300]}")
            else:
                print(f"Body: {res.text[:100]}")
        except Exception as e:
            print(f"[Method 2] Error: {e}")

if __name__ == "__main__":
    test_new_key()
