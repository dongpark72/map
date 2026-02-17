import requests

# Keys
keys = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

basis_url = "http://apis.data.go.kr/B551182/hiraInfoService/getHospBasisList"

def test_v3(key_idx, key_val):
    print(f"\n--- Testing Key {key_idx+1} (XML, No Encoding Trick) ---")
    
    # Try constructing the URL manually to ensure key format
    qs = f"serviceKey={key_val}&numOfRows=1&pageNo=1"
    full_url = f"{basis_url}?{qs}"
    
    print(f"URL: {full_url}")
    
    try:
        res = requests.get(full_url, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text[:300]}")
    except Exception as e:
        print(f"Error: {e}")

print("Running V3 Test...")
for i, k in enumerate(keys):
    test_v3(i, k)
