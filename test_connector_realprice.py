import requests
import urllib.parse
import json

def test_connector_with_realprice():
    # Test Data from views.py: Real Price
    # LAWD_CD = 11110 (Jongno-gu), DEAL_YMD = 202401
    sigungu_cd = "11110"
    ym = "202401"
    api_key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    enc_key = urllib.parse.quote(api_key)
    
    base_url = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    print(f"Testing Connector with Real Price (Jongno, {ym})")
    query = f"{base_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={ym}|numOfRows=10"
    
    try:
        res = requests.get(connector_url, params={'url': query}, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Body Start: {res.text[:500]}")
        
        if '<item>' in res.text:
            print("SUCCESS: Received data via connector!")
        else:
            print("FAILED: No items found in response.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connector_with_realprice()
