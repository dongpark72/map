import requests
import urllib.parse
import json

KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368' 
CONNECTOR_URL = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
HOSPITAL_NAME = "삼성서울병원" 
BASIS_URL_HTTP = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

def verify_and_log():
    log = []
    
    enc_key = urllib.parse.quote(KEY)
    
    # Try 1: HTTP + yadmNm directly in string
    url = BASIS_URL_HTTP
    q_basis = f"{url}^serviceKey={enc_key}|_type=json|yadmNm={HOSPITAL_NAME}|numOfRows=1|pageNo=1"
    
    log.append(f"Testing URL: {url}")
    log.append(f"Query: {q_basis}")
    
    try:
        res = requests.get(CONNECTOR_URL, params={'url': q_basis}, timeout=15, verify=False)
        log.append(f"Status: {res.status_code}")
        log.append(f"Body: {res.text[:1000]}")
        
    except Exception as e:
        log.append(f"Exception: {e}")
        
    with open("connector_debug_result.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print("Done")

if __name__ == "__main__":
    verify_and_log()
