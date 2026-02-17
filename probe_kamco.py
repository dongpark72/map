
import requests
import urllib.parse
import xml.etree.ElementTree as ET

url = "https://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
# Try http too if https fails quickly, but usually https is safer.

keys = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

# Try various parameter combinations
# Case A: Minimal
params_base = {
    "pageNo": "1",
    "numOfRows": "10"
}

# Case B: With Category
params_cat = params_base.copy()
params_cat['CTGR_HIRK_ID'] = '10000' # 주거용? 30100? Sample says 30100
params_cat['DPSL_MTD_CD'] = '0001' # 매각

# Case C: With Region
params_region = params_base.copy()
params_region['SIDO'] = '서울특별시'
params_region['SGK'] = '강남구'

def try_request(name, p, k):
    print(f"\n--- Test: {name} ---")
    p['serviceKey'] = k # Let requests handle encoding
    try:
        r = requests.get(url, params=p, timeout=5)
        print(f"URL: {r.url}")
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text[:200]}")
        if '<resultCode>00' in r.text or '<response>' in r.text:
            print("SUCCESS!!!")
            return True
    except Exception as e:
        print(f"Error: {e}")
    return False

print("Starting deep probe...")
for i, k in enumerate(keys):
    print(f"\n[Key {i+1}]")
    if try_request("Base", params_base.copy(), k): break
    if try_request("With Cat/Method", params_cat.copy(), k): break
    if try_request("With Region", params_region.copy(), k): break

    # Try manual double encoding for Key 1 just in case
    if i == 0:
        print("\n[Key 1 Double Encoded Test]")
        # Encode key manually, then pass as string in URL
        enc_k = urllib.parse.quote(k)
        qs = f"?serviceKey={enc_k}&pageNo=1&numOfRows=10"
        try:
            r = requests.get(url + qs, timeout=5)
            print(f"Manual URL: {url+qs}")
            print(f"Body: {r.text[:200]}")
        except: pass
