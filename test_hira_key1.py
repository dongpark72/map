import requests
import urllib.parse
import json

def test_hira_key1_new_url():
    # Key 1: eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==
    api_key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
    enc_key = urllib.parse.quote(api_key)
    
    hospital_name = "서울대학교병원"
    enc_hosp = urllib.parse.quote(hospital_name)
    
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    basis_url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    
    print(f"Testing HIRA Basis (Key 1, New URL) for: {hospital_name}")
    query = f"{basis_url}^serviceKey={enc_key}|_type=json|yadmNm={enc_hosp}|numOfRows=1|pageNo=1"
    
    try:
        res = requests.get(connector_url, params={'url': query}, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text[:1000]}")
        
        if 'item' in res.text:
            print("SUCCESS: Received data via connector!")
        else:
            print("FAILED: No items found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hira_key1_new_url()
