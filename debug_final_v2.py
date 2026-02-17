
import requests
import urllib.parse
import sys

# Configuration
URL = "http://openapi.onbid.co.kr/openapi/services/KamcoPblsalThingInquireSvc/getKamcoPbctCltrList"
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
SIDO = '서울특별시'
SGK = '강남구'

# Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive'
}

def test_api(mode, dpsl_code):
    print(f"\n--- Testing Mode: {mode} (DPSL={dpsl_code}) ---")
    
    # 1. requests.get with params dict (Let requests handle encoding)
    if mode == 'requests_dict':
        params = {
            'serviceKey': urllib.parse.unquote(KEY), # Pass decoded, requests will encode
            'numOfRows': '10',
            'pageNo': '1',
            'DPSL_MTD_CD': dpsl_code,
            'SIDO': SIDO,
            'SGK': SGK
        }
        try:
            r = requests.get(URL, params=params, headers=HEADERS, timeout=10)
            print(f"URL: {r.url}")
            print(f"Status: {r.status_code}")
            print(f"Body: {r.text[:500]}")
        except Exception as e:
            print(f"Error: {e}")

    # 2. Manual Query String (Double encoded key check)
    elif mode == 'manual_qs':
        # API Key is Hex, so quote/unquote doesn't change it much, but good to be safe.
        # If the server expects the key EXACTLY as provided:
        enc_key = KEY 
        
        qs = [
            f"serviceKey={enc_key}",
            f"numOfRows=10",
            f"pageNo=1",
            f"DPSL_MTD_CD={dpsl_code}",
            f"SIDO={urllib.parse.quote(SIDO)}",
            f"SGK={urllib.parse.quote(SGK)}"
        ]
        full_url = f"{URL}?{'&'.join(qs)}"
        try:
            r = requests.get(full_url, headers=HEADERS, timeout=10)
            print(f"URL: {full_url}")
            print(f"Status: {r.status_code}")
            print(f"Body: {r.text[:500]}")
        except Exception as e:
            print(f"Error: {e}")

# Run Tests
test_api('requests_dict', '0001') # Sale
test_api('manual_qs', '0001')
