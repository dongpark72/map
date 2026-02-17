import requests
import json

def test_warehouse_api():
    # Correct endpoint found from web search
    url = "https://openapi.gg.go.kr/LogisticsWarehouse"
    params = {
        "KEY": "11411d4d3b464c10a5fe57edb2917d17",
        "Type": "json",
        "pIndex": 1,
        "pSize": 5
    }
    
    try:
        print(f"Requesting to: {url}")
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 구조 확인
            if 'LogisticsWarehouse' in data:
                print("API Success!")
                rows = data['LogisticsWarehouse'][1]['row']
                if rows:
                    print(f"Total Count: {len(rows)}")
                    print("\nFirst row sample:")
                    first = rows[0]
                    print(f"Name: {first.get('CMPNM_NM')}")
                    print(f"Road Addr: {first.get('REFINE_ROADNM_ADDR')}")
                    print(f"Lat/Lon: {first.get('REFINE_WGS84_LAT')}, {first.get('REFINE_WGS84_LOGT')}")
            else:
                print("Unexpected JSON structure:")
                print(str(data)[:200])
        else:
            print(f"API Failed: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_warehouse_api()
