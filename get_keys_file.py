
import requests
import json
import sys

def get_keys_file():
    url = "https://openapi.gg.go.kr/LogisticsWarehouse"
    params = {
        "KEY": "11411d4d3b464c10a5fe57edb2917d17",
        "Type": "json",
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        row = data['LogisticsWarehouse'][1]['row'][0]
        
        with open('keys_list.txt', 'w', encoding='utf-8') as f:
            for k in row.keys():
                f.write(f"{k}\n")
                
    except Exception as e:
        print(e)

if __name__ == "__main__":
    get_keys_file()
