
import requests
import json

def check_vworld():
    pnu = "2620010300103180045" # Yeongdo 318-45
    api_key = "F78E51BE-4005-3AFF-91E0-BDDBAC8478D0"
    base_url = "https://api.vworld.kr/req/data"
    
    # 1. Building Polygon (LT_C_SPBD)
    print("--- Checking V-World Building Polygon (LT_C_SPBD) ---")
    params = {
        "service": "data",
        "request": "GetFeature",
        "data": "LT_C_SPBD",
        "key": api_key,
        "format": "json",
        "attrFilter": f"pnu:like:{pnu}",
        "domain": "http://localhost:8000",
        "size": "10"
    }
    
    try:
        res = requests.get(base_url, params=params, timeout=10)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            try:
                data = res.json()
                features = data.get('response', {}).get('result', {}).get('featureCollection', {}).get('features', [])
                print(f"Found {len(features)} building polygons.")
                for f in features:
                    props = f.get('properties', {})
                    print(f"  Name: {props.get('bul_man_no')}, Height: {props.get('bld_height')}, Floors: {props.get('flr_co')} / {props.get('und_flr_co')}")
                    # Check if there are any specific floor details? Usually NO.
                    print(f"  All Props: {props.keys()}")
            except Exception as e:
                print(f"JSON Parse Error: {e} | Text: {res.text[:100]}")
    except Exception as e:
        print(f"Request Error: {e}")

    # 2. Check Cadastral (LP_PA_CBND_BUBUN)
    print("\n--- Checking V-World Cadastral (LP_PA_CBND_BUBUN) ---")
    params['data'] = "LP_PA_CBND_BUBUN"
    try:
        res = requests.get(base_url, params=params, timeout=10)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            features = data.get('response', {}).get('result', {}).get('featureCollection', {}).get('features', [])
            print(f"Found {len(features)} land polygons.")
            if features:
                print(" -> The LAND exists in V-World.")
            else:
                print(" -> Even the LAND polygon is missing (Wrong PNU?).")
    except Exception as e:
        print(f"Land Request Error: {e}")

if __name__ == "__main__":
    check_vworld()
