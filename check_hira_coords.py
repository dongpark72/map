import requests
import json

KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

def check_coordinates():
    print("--- Checking HIRA API Response for Coordinates ---")
    
    # We will search for a hospital to see what fields are returned
    params = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '1',
        '_type': 'json',
        'yadmNm': '삼성서울병원'
    }
    
    try:
        res = requests.get(URL, params=params, timeout=10)
        data = res.json()
        item = data['response']['body']['items']['item']
        if isinstance(item, list): item = item[0]
        
        print(json.dumps(item, indent=2, ensure_ascii=False))
        
        # Check for coordinate fields
        # Common fields: XPos, YPos, xPos, yPos, lat, lng, etc.
        fields = item.keys()
        coord_fields = [f for f in fields if 'pos' in f.lower() or 'lat' in f.lower() or 'lon' in f.lower() or 'x' in f.lower() or 'y' in f.lower()]
        print(f"\nPotential Coordinate Fields: {coord_fields}")
        
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Checking HIRA API for Radius Search Support ---")
    # Trying radius parameters: xPos, yPos, radius
    # Using Samsung Seoul Hospital Approx Location: 127.085151, 37.488219 (WGS84)
    # Note: HIRA might use different coordinate system.
    
    # Let's try sending xPos, yPos, radius (typical names)
    params_rad = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '5',
        '_type': 'json',
        'xPos': '127.085151', 
        'yPos': '37.488219',
        'radius': '3000' # 3km
    }
    
    try:
        res = requests.get(URL, params=params_rad, timeout=10)
        print(f"Status (Radius): {res.status_code}")
        if res.status_code == 200:
             print(f"Body (Radius) Start: {res.text[:500]}")
             # Parse and see if we got different items
             try:
                 d = res.json()
                 items = d['response']['body']['items']['item']
                 print(f"Radius Search Result Count: {len(items) if isinstance(items, list) else 1}")
             except:
                 print("Radius search returned no items or invalid format (maybe param not supported)")
    except Exception as e:
         print(f"Error (Radius): {e}")

if __name__ == "__main__":
    check_coordinates()
