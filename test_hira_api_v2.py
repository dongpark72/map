import requests
import urllib.parse

# Keys
keys = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

basis_url = "http://apis.data.go.kr/B551182/hiraInfoService/getHospBasisList"

def test_manual(key_idx, key_val):
    print(f"\n--- Testing Key {key_idx+1} (Raw) ---")
    
    # Method 1: Let requests encode it (Standard)
    params = {
        "serviceKey": key_val,
        "_type": "json",
        "yadmNm": "서울대학교병원",
        "numOfRows": 1,
        "pageNo": 1
    }
    
    try:
        # Use a PreparedRequest to see the URL
        req = requests.Request('GET', basis_url, params=params)
        prepped = req.prepare()
        print(f"URL: {prepped.url}")
        
        s = requests.Session()
        res = s.send(prepped, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text[:300]}")
    except Exception as e:
        print(f"Error: {e}")

    # Method 2: Force Unencoded (For Key 1, this simulates typically the 'Encoding' key behavior if mislabeled)
    # But usually requests does the right thing.
    
    # Try the specific Detail endpoint too, maybe Basis list is dead
    print(f"\n--- Testing Key {key_idx+1} (Detail Endpoint) ---")
    detail_url = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7"
    # Need a valid ykiho for detail. Seoul Nat'l Hosp ykiho is roughly known or we fail.
    # Without ykiho, detail might fail. 
    # Let's stick to Basis List or check if we get a specific XML error.
    
print("Running Enhanced Test...")
for i, k in enumerate(keys):
    test_manual(i, k)
