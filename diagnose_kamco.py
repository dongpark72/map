
import requests
import sys

# URL = "http://openapi.onbid.co.kr/openapi/services/KamcoPblsalThingInquireSvc/getKamcoPbctCltrList"
URL = "http://openapi.onbid.co.kr/openapi/services/KamcoPblsalThingInquireSvc/getKamcoPbctCltrList"
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

print(f"--- Kamco Connectivity Diagnosis ---")
print(f"Target URL: {URL}")

# Test 1: Minimal (No Korean params)
print("\n[Test 1] Minimal Parameters (no SIDO/SGK)")
params_min = {
    'serviceKey': KEY,
    'numOfRows': '10',
    'pageNo': '1',
    'DPSL_MTD_CD': '0001'
}
try:
    r1 = requests.get(URL, params=params_min, timeout=15)
    print(f"Status: {r1.status_code}")
    print(f"Body: {r1.text[:300]}")
except Exception as e:
    print(f"Test 1 Failed: {e}")

# Test 2: Full Parameters (with SIDO/SGK)
print("\n[Test 2] Full Parameters (with Seoul/Gangnam)")
params_full = {
    'serviceKey': KEY,
    'numOfRows': '10',
    'pageNo': '1',
    'DPSL_MTD_CD': '0001',
    'SIDO': '서울특별시',
    'SGK': '강남구'
}
try:
    r2 = requests.get(URL, params=params_full, timeout=15)
    print(f"Status: {r2.status_code}")
    print(f"Body: {r2.text[:300]}")
except Exception as e:
    print(f"Test 2 Failed: {e}")

print("--- End of Diagnosis ---")
