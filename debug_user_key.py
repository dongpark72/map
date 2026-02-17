
import requests
import urllib.parse
import sys

# The key provided by the user
USER_KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
URL = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def test(label, key_val):
    print(f"\n--- Testing {label} ---")
    try:
        # 1. As Param (requests handles encoding)
        params = {
            "serviceKey": key_val, 
            "pageNo": "1",
            "numOfRows": "10",
            "SIDO": "서울특별시",
            "SGK": "강남구"
        }
        r1 = requests.get(URL, params=params, headers=headers, timeout=5)
        print(f"[Param] Status: {r1.status_code}")
        print(f"[Param] Body: {r1.text[:200]}")
        
    except Exception as e:
        print(f"[Param] Error: {e}")

    try:
        # 2. As Manual Query String (Encoded)
        enc = urllib.parse.quote(key_val)
        qs = f"?serviceKey={enc}&pageNo=1&numOfRows=10&SIDO={urllib.parse.quote('서울특별시')}&SGK={urllib.parse.quote('강남구')}"
        r2 = requests.get(URL + qs, headers=headers, timeout=5)
        print(f"[Manual Enc] Status: {r2.status_code}")
        print(f"[Manual Enc] Body: {r2.text[:200]}")
    except Exception as e:
        print(f"[Manual Enc] Error: {e}")

    try:
        # 3. As Manual Query String (Raw/Unencoded)
        # Use this ONLY if key has no special chars (Hex is safe)
        qs = f"?serviceKey={key_val}&pageNo=1&numOfRows=10&SIDO={urllib.parse.quote('서울특별시')}&SGK={urllib.parse.quote('강남구')}"
        r3 = requests.get(URL + qs, headers=headers, timeout=5)
        print(f"[Manual Raw] Status: {r3.status_code}")
        print(f"[Manual Raw] Body: {r3.text[:200]}")
    except Exception as e:
        print(f"[Manual Raw] Error: {e}")

test("User Key", USER_KEY)
