
import requests
import json
import sys

# Set stdout to utf-8
sys.stdout.reconfigure(encoding='utf-8')

def check_keys():
    url = "https://openapi.gg.go.kr/LogisticsWarehouse"
    params = {
        "KEY": "11411d4d3b464c10a5fe57edb2917d17",
        "Type": "json",
        "pIndex": 1,
        "pSize": 1
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        row = data['LogisticsWarehouse'][1]['row'][0]
        
        # Print all keys cleanly
        print("KEYS_START")
        for k, v in row.items():
            print(f"{k}: {v}")
        print("KEYS_END")
        
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    check_keys()
