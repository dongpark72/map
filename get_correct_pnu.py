import requests

# 카카오 API로 정확한 주소 정보 확인
address = "부산광역시 강서구 대저1동 790"

print(f"Searching for address: {address}")
print("=" * 80)

# 카카오 지도 API (Geocoding)
kakao_api_key = "{{ kakao_maps_api_key }}"  # 실제 키는 settings에서

# VWorld API로 PNU 확인
vworld_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"

url = "https://api.vworld.kr/req/address"
params = {
    "service": "address",
    "request": "getAddress",
    "key": vworld_key,
    "type": "parcel",  # 지번 주소
    "address": address,
    "format": "json"
}

try:
    res = requests.get(url, params=params, timeout=10)
    print(f"Status: {res.status_code}")
    
    if res.status_code == 200:
        data = res.json()
        print(f"\nResponse:")
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # PNU 추출
        if 'response' in data and 'result' in data['response']:
            result = data['response']['result']
            if 'items' in result and len(result['items']) > 0:
                item = result['items'][0]
                pnu = item.get('pnu')
                print(f"\n✓ Found PNU: {pnu}")
                print(f"Full address: {item.get('text', 'N/A')}")
            else:
                print("\n✗ No items found in result")
        else:
            print("\n✗ Invalid response structure")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# 다른 주소 형식도 시도
print("\n" + "=" * 80)
print("Trying alternative address formats")
print("=" * 80)

alternative_addresses = [
    "부산광역시 강서구 대저1동 790",
    "부산 강서구 대저1동 790",
    "부산광역시 강서구 대저동 790",
    "부산 강서구 대저동 790번지",
]

for addr in alternative_addresses:
    print(f"\nTrying: {addr}")
    params['address'] = addr
    try:
        res = requests.get(url, params=params, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if 'response' in data and 'result' in data['response']:
                result = data['response']['result']
                if 'items' in result and len(result['items']) > 0:
                    item = result['items'][0]
                    pnu = item.get('pnu')
                    print(f"  → PNU: {pnu}")
                    print(f"  → Full: {item.get('text', 'N/A')}")
    except:
        pass
