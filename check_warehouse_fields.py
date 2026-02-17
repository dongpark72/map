import requests
import json

def test_warehouse_api_full_fields():
    url = "https://openapi.gg.go.kr/LogisticsWarehouse"
    params = {
        "KEY": "11411d4d3b464c10a5fe57edb2917d17",
        "Type": "json",
        "pIndex": 1,
        "pSize": 2  
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'LogisticsWarehouse' in data:
                rows = data['LogisticsWarehouse'][1]['row']
                if rows:
                    print("Available Keys:", rows[0].keys())
                    print("\nSample Record:")
                    print(json.dumps(rows[0], indent=2, ensure_ascii=False))
        else:
            print("API Error")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_warehouse_api_full_fields()
