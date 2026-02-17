import requests
import urllib.parse

def test_hira_exhaustive():
    keys = [
        'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==', # Key 1 (Base64)
        'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368' # Key 2 (Hex)
    ]
    
    urls = [
         "http://apis.data.go.kr/B551182/hiraInfoService/getHospBasisList", # Old
         "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1" # New from doc
    ]
    
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    for i, key in enumerate(keys):
        enc_key = urllib.parse.quote(key)
        for url in urls:
            print(f"\n--- Testing Key {i+1}, URL: {url.split('/')[-1]} ---")
            
            # Try 1: JSON
            q_json = f"{url}^serviceKey={enc_key}|_type=json|numOfRows=1|pageNo=1"
            res_json = requests.get(connector_url, params={'url': q_json}, timeout=10)
            print(f"JSON Status: {res_json.status_code}, Body Len: {len(res_json.text)}")
            if len(res_json.text) > 0: print(f"Body: {res_json.text[:100]}")
            
            # Try 2: XML
            q_xml = f"{url}^serviceKey={enc_key}|numOfRows=1|pageNo=1"
            res_xml = requests.get(connector_url, params={'url': q_xml}, timeout=10)
            print(f"XML Status: {res_xml.status_code}, Body Len: {len(res_xml.text)}")
            if len(res_xml.text) > 0: print(f"Body: {res_xml.text[:100]}")

if __name__ == "__main__":
    test_hira_exhaustive()
