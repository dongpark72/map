
import requests
import urllib.parse
import sys

url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
key1 = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
key2 = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def test(name, key, use_manual=False):
    print(f"\n--- {name} ---")
    
    base_params = {
        "pageNo": "1", "numOfRows": "10",
        "SIDO": "서울특별시",
        "SGK": "강남구"
    }
    
    try:
        if use_manual:
            # Manual URL Assembly
            qs_parts = [f"{k}={urllib.parse.quote(v)}" for k,v in base_params.items()]
            # Key is assumed to be encoded already or needs encoding
            # If key1 (base64) -> encode it
            # If key2 (hex) -> just use it (safe)
            
            enc_key = urllib.parse.quote(key) if '=' in key else key
            qs = f"?serviceKey={enc_key}&" + "&".join(qs_parts)
            full = url + qs
            print(f"URL: {full}")
            r = requests.get(full, headers=headers, timeout=10)
        else:
            # Requests Params
            p = base_params.copy()
            p['serviceKey'] = key
            r = requests.get(url, params=p, headers=headers, timeout=10)
            print(f"URL: {r.url}")

        print(f"Status: {r.status_code}")
        print(f"Body: {r.text[:300]}")
        
    except Exception as e:
        print(e)

test("Key 1 (Requests)", key1, False)
test("Key 1 (Manual Encoded)", key1, True)
test("Key 2 (Requests)", key2, False)
test("Key 2 (Manual)", key2, True)
