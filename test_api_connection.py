import requests
import urllib.parse
import json

# Keys from views.py
keys = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

def test_hira_basis(key, key_name):
    url = "http://apis.data.go.kr/B551182/hiraInfoService/getHospBasisList"
    # Test 1: Passing key as param (Requests will encode it)
    print(f"\n[{key_name}] Testing HIRA Basis (Standard Params)...")
    try:
        params = {
            "serviceKey": key,
            "_type": "json",
            "numOfRows": 1,
            "pageNo": 1
        }
        res = requests.get(url, params=params, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 2: Passing raw key in URL (No extra encoding if we construct string carefully)
    print(f"\n[{key_name}] Testing HIRA Basis (Manual URL)...")
    try:
        # If key is already encoded (ends with ==), we might want to send it as is.
        # But if we put it in f-string, requests might not touch it if we use string url?
        # Actually requests.get(url) where url includes params.
        
        # NOTE: requests.get(full_url) might still re-encode if not careful, but let's try.
        # We need to manually construct query string.
        # But wait, standard browser includes key as `serviceKey=...`
        # If key is `...==`, browser sends `...%3D%3D`.
        
        qs = f"serviceKey={key}&_type=json&numOfRows=1&pageNo=1"
        full_url = f"{url}?{qs}"
        res = requests.get(full_url, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

def test_real_price(key, key_name):
    # APT Trade
    url = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"
    print(f"\n[{key_name}] Testing Real Price (APT)...")
    
    # Needs LAWD_CD and DEAL_YMD
    params = {
        "serviceKey": key,
        "LAWD_CD": "11110", # Jongno-gu
        "DEAL_YMD": "202401",
        "numOfRows": 1
    }
    
    try:
        res = requests.get(url, params=params, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

print("=== STARTING CONNECTION TESTS ===")
for i, key in enumerate(keys):
    name = f"Key {i+1}"
    test_hira_basis(key, name)
    test_real_price(key, name)
    
    # Try decoding Key 1 too, just in case
    if "==" in key:
        try:
            decoded_key = urllib.parse.unquote(key) 
            # Wait, unquote is for % encoding. 
            # If it is Base64, we treat it as the "Decoded" service key in portal terms sometimes?
            # Actually, Portal gives "Encoding" and "Decoding" keys.
            # "Encoding" key is the one we use in HTTP GET usually (already has % if needed?? No, usually it's Base64).
            
            # Let's try sending the key Unquoted if it was % encoded?
            # eLT...== is Base64. It contains no %. 
            pass
        except:
            pass
