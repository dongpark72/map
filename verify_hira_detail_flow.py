import requests
import json

# Config
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
BASIS_URL = "https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
DETAIL_URL = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7" # 시설정보(병상수)

def verify_full_flow():
    print("--- 1. Get YKIHO (Basis Service) ---")
    params_name = {
        'serviceKey': KEY,
        '_type': 'json',
        'yadmNm': '삼성서울병원',
        'pageNo': '1',
        'numOfRows': '1'
    }
    
    ykiho = None
    try:
        res = requests.get(BASIS_URL, params=params_name, timeout=10, verify=False) # Skip SSL verify for test
        if res.status_code == 200:
            data = res.json()
            items = data['response']['body']['items']['item']
            if isinstance(items, list): items = items[0]
            ykiho = items['ykiho']
            print(f"Got YKIHO: {ykiho}")
        else:
            print(f"Basis Error: {res.status_code} {res.text}")
            return
    except Exception as e:
        print(f"Basis Exception: {e}")
        return

    print("\n--- 2. Get Facility Info (Detail Service: getEqpInfo2.7) ---")
    params_detail = {
        'serviceKey': KEY,
        '_type': 'json',
        'ykiho': ykiho,
        'pageNo': '1',
        'numOfRows': '1'
    }
    
    try:
        res2 = requests.get(DETAIL_URL, params=params_detail, timeout=10, verify=False)
        print(f"Status: {res2.status_code}")
        if res2.status_code == 200:
            print("Raw Detail Response (First 500 chars):")
            print(res2.text[:500])
            
            try:
                data2 = res2.json()
                print("\nParsed JSON Structure Keys:")
                print(data2.keys())
                
                # Check items
                if 'response' in data2 and 'body' in data2['response']:
                     body = data2['response']['body']
                     if 'items' in body:
                         items_wrapper = body['items']
                         print("\nItems content:")
                         print(items_wrapper)
                     else:
                         print("No 'items' in body")
            except Exception as e:
                print(f"JSON Parse Error: {e}")
        else:
            print(f"Detail Error Body: {res2.text}")
            
    except Exception as e:
        print(f"Detail Exception: {e}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    verify_full_flow()
