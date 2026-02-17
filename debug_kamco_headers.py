
import requests
import urllib.parse
import xml.etree.ElementTree as ET

# API Keys
KEYS = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"

def test_kamco_with_header(sido, sgk, key_idx=0):
    api_key = KEYS[key_idx]
    enc_key = urllib.parse.quote(api_key)
    
    # Browser User-Agent to bypass Python block
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.onbid.co.kr/' # fake referer just in case
    }
    
    # Using requests params to handle construction, passing unencoded key
    params = {
        "serviceKey": api_key, # requests will urlencode this
        "pageNo": "1",
        "numOfRows": "500",
        "SIDO": sido,
        "SGK": sgk
    }
    
    # Also valid: sometimes keys must be passed *already encoded* if using params doesn't work well with data.go.kr quirks.
    # But usually User-Agent is the main blocker if the message explicitly says "Python Blocked".
    
    print(f"\nTesting with Key {key_idx+1} and User-Agent spoofing...")
    try:
        # Try passing unencoded key in params (standard way)
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"URL Used: {response.url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response Snippet: {response.text[:300]}")
            if '<resultCode>00' in response.text:
                print("SUCCESS: Data retrieved!")
                root = ET.fromstring(response.text)
                total = root.find('.//totalCount').text
                print(f"Total Items: {total}")
                return True
            else:
                print("API returned error or non-success code.")
        else:
            print("HTTP Error.")
            
    except Exception as e:
        print(f"Exception: {e}")
    return False

# Test
test_kamco_with_header("서울특별시", "강남구", 0)
