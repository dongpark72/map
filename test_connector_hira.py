import requests
import urllib.parse
import xml.etree.ElementTree as ET

keys = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

def test_hira_via_connector(key, key_idx):
    print(f"\n[{key_idx}] Testing HIRA via Connector...")
    
    # Target URL (HIRA Basis)
    target_url = "http://apis.data.go.kr/B551182/hiraInfoService/getHospBasisList"
    
    # Connector URL
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # Encode key for Connector param
    enc_key = urllib.parse.quote(key)
    
    # Construct piped query for Connector
    # Format: url^param1=val1|param2=val2...
    # Note: Connector usually expects the ServiceKey provided as part of the piped string
    
    # We want info for a hospital that exists.
    # From views.py: yadmNm=hospital_name
    # Let's pick a common hospital name or just list basic ones
    hospital_name = "서울대학교병원"
    enc_hospital_name = urllib.parse.quote(hospital_name) # Double encode? No, Connector might handle.
    # Usually Connector takes params as is. But Korean chars might need encoding?
    # In views.py: 
    # q_recap = f"{api_url}^serviceKey={enc_key}|..."
    # No extra encoding for values usually, requests handles it?
    # Wait, 'requests.get(connector_url, params={'url': query})'
    # So 'query' string is passed as 'url' parameter.
    
    # Let's try explicit encoding for Hangle
    
    query = f"{target_url}^serviceKey={enc_key}|_type=json|numOfRows=1|pageNo=1"
    
    # Add hospital name if testing search
    # query += f"|yadmNm={hospital_name}" 
    # NOTE: If we put hangle in query string, we should ensure it's safe. 
    # But for a simple test, let's just list 1 item (without filtering name) to see if it works.
    
    print(f"Query: {query}")
    
    try:
        res = requests.get(connector_url, params={'url': query}, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:300]}")
    except Exception as e:
        print(f"Error: {e}")

print("=== STARTING CONNECTOR TESTS ===")
for i, key in enumerate(keys):
    test_hira_via_connector(key, f"Key {i+1}")
