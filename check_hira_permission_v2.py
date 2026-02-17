import requests
import urllib.parse
import json

# 올바른 키 (Base64)
API_KEY = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='

# EUM Connector URL
CONNECTOR_URL = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"

# Target HIRA URL
BASIS_URL = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"

# Target Hospital Name (e.g., 동탄아이엠유의원 - likely to exist, or use a very common one like '서울대학교병원' for test)
# '동탄아이엠유의원' might be too specific or changed. Let's try '삼성서울병원'
HOS_NAME = "삼성서울병원" 

def check_via_proxy():
    print("--- Testing via UrlConnector with Correct Key ---")
    
    # Key Encoding
    enc_key = urllib.parse.quote(API_KEY)
    
    # Construct 'url' parameter string for the connector
    # Connector syntax seems to be: URL^param1=val1|param2=val2...
    # Note: We should see if 'yadmNm' needs encoding. usually requests handles encoding of params values, 
    # but here 'yadmNm' is part of the 'url' param value string. So we might need to double-encode or just one-encode.
    # The connector likely splits by '|' and appends query string.
    
    # Try 1: yadmNm raw (requests will encode it as part of 'url' value)
    # q_str = f"{BASIS_URL}^serviceKey={enc_key}|_type=json|yadmNm={HOS_NAME}|numOfRows=1|pageNo=1"
    
    # But wait, python requests 'params' will percent-encode 'HOS_NAME' when making the request to Connector.
    # The Connector then receives it. Does it forward it encoded?
    # Let's try just letting requests handle the outer encoding.
    
    q_str = f"{BASIS_URL}^serviceKey={enc_key}|_type=json|yadmNm={HOS_NAME}|numOfRows=1|pageNo=1"
    
    print(f"Query String for Connector: {q_str}")
    
    try:
        res = requests.get(CONNECTOR_URL, params={'url': q_str}, timeout=15, verify=False)
        print(f"Status: {res.status_code}")
        print(f"Headers: {res.headers}")
        print(f"Body: {res.text[:1000]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_via_proxy()
