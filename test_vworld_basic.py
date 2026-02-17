import requests
import json

KEY = "F78E51BE-4005-3AFF-91E0-BDDBAC8478D0"
DOMAIN = "localhost" # or the server IP
PNU = "2671025028100080001"

def fetch_vworld(layer, pnu_field="pnu"):
    url = "https://api.vworld.kr/req/data"
    params = {
        "service": "data",
        "request": "GetFeature",
        "data": layer,
        "key": KEY,
        "domain": DOMAIN,
        "attrFilter": f"{pnu_field}:=:{PNU}",
        "format": "json",
        "size": "10",
        "buffer": "2" # Sometimes needed
    }
    
    try:
        res = requests.get(url, params=params, timeout=5)
        print(f"--- Layer: {layer} ---")
        if res.status_code == 200:
            data = res.json()
            if "response" in data and data["response"]["status"] == "OK":
                feats = data["response"]["result"]["featureCollection"]["features"]
                print(f"Found {len(feats)} features")
                if feats:
                    print(json.dumps(feats[0]["properties"], indent=2, ensure_ascii=False))
            else:
                print("No Data or Error:", data)
        else:
            print(f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # 1. Cadastral (Basic Info: Area, Jimok)
    fetch_vworld("LP_PA_CBND_BUBUN") 
    
    # 2. Land Price (Gongsi Jiga) -> DT_166 (IndvdLandPrice) or similar? 
    # Checking common layer names for price. 
    # Let's try to search via keyword if needed, but I'll try known codes.
    # Note: VWorld recently changed some service codes. 
    pass
