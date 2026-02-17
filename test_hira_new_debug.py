import requests
import urllib.parse
import json

# API Keys from .env
PUBLIC_DATA_KEYS = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

def test_hira_basis_connector():
    # .env's PUBLIC_DATA_KEY_2 (ending in ...70b551099368) matches the user's screenshot
    api_key = PUBLIC_DATA_KEYS[1]
    enc_key = urllib.parse.quote(api_key)
    
    # New endpoints from user screenshots
    basis_url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    hospital_name = "동탄아이엠유의원"
    
    # Try different query formats for Hangle
    # Format A: Plain hangle in query (How views.py currently does it)
    q_basis = f"{basis_url}^serviceKey={enc_key}|_type=json|yadmNm={hospital_name}|numOfRows=1|pageNo=1"
    
    print(f"Testing Basis Connector with name: {hospital_name}")
    print(f"Query: {q_basis}")
    
    try:
        res = requests.get(connector_url, params={'url': q_basis}, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Content-Type: {res.headers.get('Content-Type')}")
        print(f"Raw Response (first 500 chars):\n{res.text[:500]}")
        
        try:
            data = res.json()
            print("JSON Parse: SUCCESS")
            items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            print(f"Items found: {len(items) if isinstance(items, list) else 1 if items else 0}")
        except:
            print("JSON Parse: FAILED")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hira_basis_connector()
