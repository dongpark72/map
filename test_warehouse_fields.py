import requests
import json

# 경기도 물류창고 API 테스트
api_key = '11411d4d3b464c10a5fe57edb2917d17'
url = "https://openapi.gg.go.kr/LogisticsWarehouse"

params = {
    "KEY": api_key,
    "Type": "json",
    "pIndex": 1,
    "pSize": 10,
    "SIGUN_NM": "수원시"  # 수원시로 테스트
}

try:
    print("Fetching warehouse data from API...")
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        # 구조 확인
        print(f"\nResponse keys: {data.keys()}\n")
        
        if 'LogisticsWarehouse' in data:
            warehouse_data = data['LogisticsWarehouse']
            
            if isinstance(warehouse_data, list) and len(warehouse_data) > 1:
                # 첫 번째는 메타데이터, 두 번째부터 실제 데이터
                meta = warehouse_data[0]
                print(f"Total count: {meta.get('head', [{}])[1].get('list_total_count', 'N/A')}")
                
                items = warehouse_data[1].get('row', [])
                print(f"\nFound {len(items)} warehouse items\n")
                
                # 첫 번째 아이템의 모든 필드 출력
                if items:
                    print("="*80)
                    print("First item - All fields:")
                    print("="*80)
                    first_item = items[0]
                    for key, value in sorted(first_item.items()):
                        print(f"{key}: {value}")
                    
                    print("\n" + "="*80)
                    print("Sample items (key fields):")
                    print("="*80)
                    
                    for idx, item in enumerate(items[:5], 1):
                        print(f"\n--- Warehouse {idx} ---")
                        print(f"사업장명: {item.get('BIZPLC_NM', 'N/A')}")
                        print(f"인허가일자: {item.get('LICENSG_DE', 'N/A')}")
                        print(f"주소: {item.get('REFINE_ROADNM_ADDR', 'N/A')}")
                        print(f"보관요율 (CUSTODY_TARIFF_RT): '{item.get('CUSTODY_TARIFF_RT', 'N/A')}'")
                        print(f"업태명 (INDUTY_NM): '{item.get('INDUTY_NM', 'N/A')}'")
                        print(f"업종명 (ITEM_NM): '{item.get('ITEM_NM', 'N/A')}'")
                        
                        # 다른 가능한 필드명들도 확인
                        for key in item.keys():
                            if '요율' in key or '업태' in key or '업종' in key:
                                print(f"  -> {key}: {item[key]}")
        else:
            print("Unexpected response structure")
            print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Error: HTTP {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
