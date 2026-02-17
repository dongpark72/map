
import requests
import urllib.parse
import xml.etree.ElementTree as ET

KEYS = [
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368',
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
]

def test_kamco_filter(ctgr_id, key_idx):
    # Try both URLs
    urls = [
        "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr",
        "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
    ]
    key = KEYS[key_idx]
    
    for url in urls:
        print(f"\nTesting URL: {url} with Key Index {key_idx}")
        enc_key = urllib.parse.quote(key) if key_idx == 1 else key # Hex keys might not need encoding or are already encoded
        
        query_params = [
            f"serviceKey={enc_key}",
            f"numOfRows=5",
            f"pageNo=1",
            f"DPSL_MTD_CD=0001",
            f"SIDO={urllib.parse.quote('경기도')}",
        ]
        if ctgr_id:
            query_params.append(f"CTGR_ID={ctgr_id}")
        
        full_url = f"{url}?{'&'.join(query_params)}"
        try:
            response = requests.get(full_url, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            if '<resultCode>00</resultCode>' in response.text:
                print("SUCCESS!")
                return True
        except Exception as e:
            print(f"Error: {e}")
    return False

print("--- Testing Key 0 ---")
test_kamco_filter("10000", 0)
print("\n--- Testing Key 1 ---")
test_kamco_filter("10000", 1)
