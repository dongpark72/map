import requests
import json

def test_hira_direct_https():
    # Key 2: e273fd... (Hex)
    api_key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    
    hospital_name = "연세로의료의원"
    
    # NEW URL with HTTPS
    basis_url = "https://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    
    params = {
        'serviceKey': api_key,
        '_type': 'json',
        'yadmNm': hospital_name,
        'numOfRows': 1,
        'pageNo': 1
    }
    
    print(f"Testing HIRA Direct HTTPS for: {hospital_name}")
    try:
        # We need to be careful with serviceKey encoding here if requests encodes it again.
        # But for Hex keys, encoding usually doesn't change it.
        res = requests.get(basis_url, params=params, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:500]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hira_direct_https()
