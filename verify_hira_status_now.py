import requests
import json
import urllib.parse

# Config
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
BASE_URL = "https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

def test_hira_live():
    print("--- Testing HIRA API Live Connection ---")
    
    # 1. Test by Name (Samsung Seoul Hospital)
    print("\n1. Testing Search by Name (삼성서울병원)...")
    params_name = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '1',
        '_type': 'json',
        'yadmNm': '삼성서울병원'
    }
    try:
        res = requests.get(BASE_URL, params=params_name, timeout=10)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            try:
                data = res.json()
                items = data['response']['body']['items']['item']
                print("Success! Data preview:")
                print(str(items)[:100] + "...")
                ykiho = items.get('ykiho') if isinstance(items, dict) else items[0].get('ykiho')
                print(f"Captured YKIHO: {ykiho}")
            except Exception as e:
                print(f"JSON Parse Error: {e}")
                print(res.text[:200])
        else:
            print(res.text[:200])
    except Exception as e:
        print(f"Connection Error: {e}")

    # 2. Test by Radius (Coordinates from user screenshot or known location)
    # Hanam example: 127.1, 37.5
    print("\n2. Testing Search by Radius (x=127.177, y=37.555, r=3000)...")
    params_radius = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '5',
        '_type': 'json',
        'xPos': '127.177',
        'yPos': '37.555',
        'radius': '3000'
    }
    try:
        res = requests.get(BASE_URL, params=params_radius, timeout=10)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
             try:
                data = res.json()
                items = data['response']['body']['items']['item']
                count = len(items) if isinstance(items, list) else 1
                print(f"Success! Found {count} hospitals.")
             except Exception as e:
                print(f"JSON Parse Error or No Items: {e}")
                print(res.text[:200])
        else:
            print(res.text[:200])
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_hira_live()
