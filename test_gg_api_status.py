import requests
import json

# Gyeonggi Data Dream API Endpoint for Logistics Warehouse
# Replace KEY with your actual key if different
KEY = '5b65377f06534927b20464a66a1e9447' 
URL = "https://openapi.gg.go.kr/LogisticsWarehouse"

def test_gg_api_status():
    print(f"Testing Gyeonggi Data Dream API: {URL}")
    params = {
        'KEY': KEY,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 5,
        'SIGUN_NM': '하남시'  # Test with a specific region
    }
    
    try:
        response = requests.get(URL, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        try:
            data = response.json()
            # print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if 'LogisticsWarehouse' in data:
                head = data['LogisticsWarehouse'][0].get('head')
                if head:
                     print(f"API Response Head: {head}")
                     return True, "API seems operational."
            elif 'RESULT' in data:
                 print(f"API Error Result: {data['RESULT']}")
                 return False, f"API returned error: {data['RESULT']}"
            else:
                 print("Unknown response structure.")
                 print(data)
                 return False, "Unknown structure"

        except json.JSONDecodeError:
            print("Failed to decode JSON. Response text preview:")
            print(response.text[:500])
            return False, "Invalid JSON response (Server might be down returning HTML)"
            
    except Exception as e:
        print(f"Connection Error: {e}")
        return False, str(e)

if __name__ == "__main__":
    test_gg_api_status()
