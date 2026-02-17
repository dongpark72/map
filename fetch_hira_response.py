import requests
import urllib.parse
import re

PUBLIC_DATA_KEYS = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

def fetch_to_file():
    api_key = PUBLIC_DATA_KEYS[1]
    enc_key = urllib.parse.quote(api_key)
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # 1. Basis
    basis_url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    hospital_name = "동탄아이엠유의원"
    q_basis = f"{basis_url}^serviceKey={enc_key}|_type=json|yadmNm={hospital_name}|numOfRows=1|pageNo=1"
    
    print("Fetching Basis...")
    try:
        res = requests.get(connector_url, params={'url': q_basis}, timeout=10)
        with open("hira_basis_response.xml", "w", encoding="utf-8") as f:
            f.write(res.text)
        print("Saved hira_basis_response.xml")
        
        # Find ykiho using regex
        match = re.search(r'<ykiho>(.*?)</ykiho>', res.text)
        if match:
            ykiho = match.group(1)
            print(f"Found ykiho: {ykiho}")
            
            # 2. Detail
            detail_url = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7"
            q_detail = f"{detail_url}^serviceKey={enc_key}|_type=json|ykiho={ykiho}|numOfRows=1|pageNo=1"
            
            print("Fetching Detail...")
            res2 = requests.get(connector_url, params={'url': q_detail}, timeout=10)
            with open("hira_detail_response.xml", "w", encoding="utf-8") as f:
                f.write(res2.text)
            print("Saved hira_detail_response.xml")
            
        else:
            print("ykiho not found in response.")
            # Also try to see if it's in JSON format in the text
            match_json = re.search(r'"ykiho":"(.*?)"', res.text)
            if match_json:
                ykiho = match_json.group(1)
                print(f"Found ykiho in JSON: {ykiho}")
                
                detail_url = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7"
                q_detail = f"{detail_url}^serviceKey={enc_key}|_type=json|ykiho={ykiho}|numOfRows=1|pageNo=1"
                
                print("Fetching Detail (from JSON ykiho)...")
                res2 = requests.get(connector_url, params={'url': q_detail}, timeout=10)
                with open("hira_detail_response.xml", "w", encoding="utf-8") as f:
                    f.write(res2.text)
                print("Saved hira_detail_response.xml")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_to_file()
