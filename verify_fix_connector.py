import requests
import urllib.parse
import json

# Mimic maps/views.py configuration
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368' # Key 2
CONNECTOR_URL = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
HOSPITAL_NAME = "삼성서울병원" 

# Candidates
BASIS_URL_HTTPS = "https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
BASIS_URL_HTTP = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

def verify_fix_via_connector():
    print("--- Verifying Fix via UrlConnector ---")
    
    enc_key = urllib.parse.quote(KEY)
    
    for url in [BASIS_URL_HTTPS, BASIS_URL_HTTP]:
        print(f"\nTargeting: {url}")
        
        # Query String format for Connector
        q_basis = f"{url}^serviceKey={enc_key}|_type=json|yadmNm={HOSPITAL_NAME}|numOfRows=1|pageNo=1"
        
        try:
            res = requests.get(CONNECTOR_URL, params={'url': q_basis}, timeout=15, verify=False)
            print(f"Connector Status: {res.status_code}")
            
            if res.status_code == 200:
                print(f"Body Start: {res.text[:300]}")
                if '"response":' in res.text and '"items":' in res.text:
                     print(">>> SUCCESS! valid JSON response found.")
                elif '<response>' in res.text and '<items>' in res.text:
                     print(">>> SUCCESS! valid XML response found.")
                else:
                     print(">>> RESPONSE CONTENT UNKNOWN (Might be auth error or empty)")
            else:
                print(f"Error Status: {res.status_code}")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    verify_fix_via_connector()
