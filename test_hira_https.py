import requests
import urllib.parse
import json

def test_hira_https_connector():
    # Use HTTPS for BOTH
    api_key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    enc_key = urllib.parse.quote(api_key)
    
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    basis_url = "https://apis.data.go.kr/B551182/hiraInfoService/getHospBasisList"
    
    print("Testing HIRA Basis with HTTPS via Connector")
    # Try WITHOUT _type=json first to see if XML works
    query = f"{basis_url}^serviceKey={enc_key}|numOfRows=1|pageNo=1"
    
    try:
        res = requests.get(connector_url, params={'url': query}, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text[:1000]}")
        
        if '<response>' in res.text or '<item>' in res.text:
            print("SUCCESS: Received data via connector (XML)!")
        elif '{' in res.text:
            print("SUCCESS: Received JSON!")
        else:
            print("FAILED: No items found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hira_https_connector()
