import requests
import urllib.parse
import json

def verify_hospital():
    # Key from user observation
    key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    enc_key = urllib.parse.quote(key)
    connector = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    basis_url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    
    # 1. Test strictly with the name from the screenshot
    target_name = "서울특별시서울의료원"
    
    # Strategy A: Raw String (Current implementation)
    q_a = f"{basis_url}^serviceKey={enc_key}|_type=json|yadmNm={target_name}|numOfRows=1|pageNo=1"
    
    # Strategy B: Encoded String
    enc_name = urllib.parse.quote(target_name)
    q_b = f"{basis_url}^serviceKey={enc_key}|_type=json|yadmNm={enc_name}|numOfRows=1|pageNo=1"
    
    print(f"--- Testing Target: {target_name} ---")
    
    print("\n[Strategy A: Raw String]")
    try:
        res = requests.get(connector, params={'url': q_a}, timeout=10, verify=False)
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text[:300]}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n[Strategy B: Encoded String]")
    try:
        res = requests.get(connector, params={'url': q_b}, timeout=10, verify=False)
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text[:300]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_hospital()
