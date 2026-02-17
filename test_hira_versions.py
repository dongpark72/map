import requests
import urllib.parse

KEY = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='

# Possible Endpoints
ENDPOINTS = [
    "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1", # Original
    "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList",  # Without 1 (Common pattern)
    "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList",   # Service without 1
    "http://apis.data.go.kr/B551182/hospitalInfoService/getHospitalBasisList", # English full name guess?
]

def test_endpoints():
    encoded_key = urllib.parse.quote(KEY)
    
    for url in ENDPOINTS:
        print(f"\n--- Testing Endpoint: {url} ---")
        full_url = f"{url}?ServiceKey={encoded_key}&pageNo=1&numOfRows=1&_type=json"
        
        try:
            res = requests.get(full_url, timeout=5)
            print(f"Status: {res.status_code}")
            if res.status_code != 404:
                print(f"Body: {res.text[:300]}")
            else:
                print("Body: 404 Not Found")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_endpoints()
