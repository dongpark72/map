import requests
import json
import codecs
import sys

# Windows 인코딩 이슈 해결을 위한 stdout 재설정
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

def check_coordinates_v2():
    print("--- Checking HIRA API Response for Coordinates ---")
    
    # Radius Test Params
    params_rad = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '5',
        '_type': 'json',
        'xPos': '127.085151', 
        'yPos': '37.488219',
        'radius': '3000' # 3km
    }
    
    target_fields = []
    
    try:
        res = requests.get(URL, params=params_rad, timeout=10)
        print(f"Status: {res.status_code}")
        
        if res.status_code == 200:
             data = res.json()
             items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
             
             if not items:
                 print("No items found.")
                 return

             first_item = items[0] if isinstance(items, list) else items
             
             # 좌표 관련 필드 찾기
             print("\n[One Item Keys and Values]")
             for k, v in first_item.items():
                 # 좌표 관련 키워드
                 if any(sub in k.lower() for sub in ['x', 'y', 'lat', 'lon', 'pos', 'addr']):
                     print(f"  {k}: {v}")
                     target_fields.append(k)
                     
             print(f"\nFound {len(items) if isinstance(items, list) else 1} items.")
             print(f"Has X/Y? : {'YES' if any(f in target_fields for f in ['XPos', 'YPos', 'xPos', 'yPos']) else 'NO'}")

    except Exception as e:
         print(f"Error: {e}")

if __name__ == "__main__":
    check_coordinates_v2()
