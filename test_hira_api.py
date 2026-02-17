import requests
import urllib.parse
import json

# Keys from views.py
keys = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

def test_key(index, api_key):
    print(f"\n--- Testing Key {index + 1} ---")
    print(f"Key: {api_key[:20]}...")
    
    # 1. Test getHospBasisList (Hospital Basis Info)
    basis_url = "http://apis.data.go.kr/B551182/hiraInfoService/getHospBasisList"
    
    # Try with decoded key first (requests will encode it)
    try:
        decoded_key = urllib.parse.unquote(api_key)
    except:
        decoded_key = api_key

    params = {
        "serviceKey": decoded_key, # requests will encode this
        "_type": "json",
        "yadmNm": "서울대학교병원", # Test with a famous hospital
        "numOfRows": 1,
        "pageNo": 1
    }
    
    try:
        print(f"Requesting {basis_url}...")
        res = requests.get(basis_url, params=params, timeout=10)
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text[:300]}")
        
        if res.status_code == 200:
            try:
                data = res.json()
                if 'response' in data and 'header' in data['response']:
                    result_code = data['response']['header'].get('resultCode')
                    result_msg = data['response']['header'].get('resultMsg')
                    print(f"API Result: {result_code} - {result_msg}")
                    return result_code == '00'
                else:
                    print("Unexpected JSON structure.")
            except:
                print("Response is not JSON.")
    except Exception as e:
        print(f"Error: {e}")
    
    return False

print("Starting API Key Test...")
requests.packages.urllib3.disable_warnings() # Disable SSL warnings just in case

for i, key in enumerate(keys):
    result = test_key(i, key)
    if result:
        print(f"\n[SUCCESS] Key {i+1} seems to be WORKING.")
    else:
        print(f"\n[FAILURE] Key {i+1} seems to valid or unauthorized.")
