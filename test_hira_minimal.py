import requests
import urllib.parse

def test_hira_minimal():
    # Key 2: e273fd...
    api_key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    enc_key = urllib.parse.quote(api_key)
    
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    # New Doc URL
    basis_url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    
    print("Testing HIRA Minimal (Listing top 10)")
    # NO _type=json, NO yadmNm
    query = f"{basis_url}^serviceKey={enc_key}|numOfRows=10|pageNo=1"
    
    try:
        res = requests.get(connector_url, params={'url': query}, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text[:1000]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hira_minimal()
