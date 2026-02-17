import requests
import urllib.parse
import json

def test_hira_new_doc_url():
    # From Image 1: http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1
    # Note: Images show http, but apis.data.go.kr usually supports https too.
    api_key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    enc_key = urllib.parse.quote(api_key)
    
    hospital_name = "서울대학교병원"
    
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    # Exact URL from image 1
    basis_url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    
    print(f"Testing HIRA Basis (New Doc logic) for: {hospital_name}")
    # Internal parameters are NOT encoded because the whole 'url' param will be encoded by requests.get
    query = f"{basis_url}^serviceKey={enc_key}|_type=json|yadmNm={hospital_name}|numOfRows=1|pageNo=1"
    
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
    test_hira_new_doc_url()
