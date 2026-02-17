import requests
import urllib.parse
import json

KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
BASIS_URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
DETAIL_URL = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7"
HOSPITAL_NAME = "삼성서울병원"

def test_direct_flow():
    print(f"--- 1. Basis Info (Direct) ---")
    params = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '1',
        '_type': 'json',
        'yadmNm': HOSPITAL_NAME
    }
    
    ykiho = None
    try:
        res = requests.get(BASIS_URL, params=params, timeout=10)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            items = data['response']['body']['items']['item']
            if isinstance(items, list):
                item = items[0]
            else:
                item = items
            ykiho = item.get('ykiho')
            print(f"Found ykiho: {ykiho}")
        else:
            print(f"Failed: {res.text[:200]}")
            return
            
    except Exception as e:
        print(f"Error: {e}")
        return

    if not ykiho:
        print("No ykiho found.")
        return

    print(f"\n--- 2. Detail Info (Direct) ---")
    # For Detail info, standard params
    d_params = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '1',
        '_type': 'json',
        'ykiho': ykiho
    }
    
    try:
        # Detail URL is HTTPS. Verify=False for safety against cert issues on this env
        res = requests.get(DETAIL_URL, params=d_params, verify=False, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text[:300]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_direct_flow()
