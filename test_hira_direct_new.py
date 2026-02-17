import requests
import urllib.parse
import json

def test_hira_direct_new_url():
    # From Image 1: http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1
    api_key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
    
    hospital_name = "서울대학교병원" # Use a very common one for testing
    
    basis_url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    
    # Try with params (requests handles encoding)
    params = {
        'serviceKey': api_key,
        '_type': 'json',
        'yadmNm': hospital_name,
        'numOfRows': 1,
        'pageNo': 1
    }
    
    print(f"Testing HIRA Basis Direct for: {hospital_name}")
    try:
        res = requests.get(basis_url, params=params, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Response Head: {res.text[:500]}")
        
        if res.status_code == 200:
            try:
                data = res.json()
                print("SUCCESS: Received JSON data!")
            except:
                print("Received non-JSON response.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hira_direct_new_url()
