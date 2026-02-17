
import requests
import urllib.parse
import xml.etree.ElementTree as ET

url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
KEYS = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def run_test(name, params):
    print(f"\n--- Test: {name} ---")
    try:
        # Use Key 1 Decoded
        params['serviceKey'] = KEYS[0]
        r = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text[:300]}")
    except Exception as e:
        print(e)

# Case 1: Add Category (Property)
run_test("Category 10000 (Property?)", {
    "pageNo": "1", "numOfRows": "10",
    "CTGR_HIRK_ID": "10000" 
})

# Case 2: Add Disposal Method (Sale?)
run_test("Disposal Method 0001", {
    "pageNo": "1", "numOfRows": "10",
    "DPSL_MTD_CD": "0001"
})

# Case 3: Both
run_test("Cat + Disposal", {
    "pageNo": "1", "numOfRows": "10",
    "CTGR_HIRK_ID": "10000",
    "DPSL_MTD_CD": "0001"
})

# Case 4: Search specific known item (Gaepo-dong) without region to see if it works
run_test("Keyword Search", {
    "pageNo": "1", "numOfRows": "10",
    "GOODS_NM": "개포동"
})
