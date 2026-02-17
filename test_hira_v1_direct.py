import requests
import urllib.parse

key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
params = {
    'serviceKey': key,
    'pageNo': '1',
    'numOfRows': '1',
    '_type': 'json'
}

print(f"Testing {url} with key ending in ...{key[-5:]}")

try:
    # Try sending key as is (requests might encode it, but let's see)
    res = requests.get(url, params=params, timeout=10)
    print(f"Status: {res.status_code}")
    print(f"Body: {res.text[:300]}")
except Exception as e:
    print(f"Error: {e}")

print("-" * 20)

# Try with encoded key manually
quoted_key = urllib.parse.quote(key)
qs = f"serviceKey={quoted_key}&pageNo=1&numOfRows=1&_type=json"
full_url = f"{url}?{qs}"
print(f"Testing manually constructed URL: {full_url}")

try:
    res = requests.get(full_url, timeout=10)
    print(f"Status: {res.status_code}")
    print(f"Body: {res.text[:300]}")
except Exception as e:
    print(f"Error: {e}")
