
import requests
import json
import sys

# Set stdout to utf-8
sys.stdout.reconfigure(encoding='utf-8')

def check_specific_fields():
    # 데이터 확인용: pSize를 늘려서 유의미한 데이터가 있는지 확인
    url = "https://openapi.gg.go.kr/LogisticsWarehouse"
    params = {
        "KEY": "11411d4d3b464c10a5fe57edb2917d17",
        "Type": "json",
        "pIndex": 1,
        "pSize": 50 
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        rows = data['LogisticsWarehouse'][1]['row']
        
        print("Checking Fields Data Summary (Sample 50 items)...")
        
        tariff_samples = []
        biz_samples = []
        
        for row in rows:
            t = row.get('CUSTODY_TARIFF_RT')
            b = row.get('BIZCOND_CUSTODY_ND_WAREHS_NM')
            
            if t: tariff_samples.append(t)
            if b: biz_samples.append(b)
            
        print(f"\nCUSTODY_TARIFF_RT (Not None Count: {len(tariff_samples)}):")
        print(tariff_samples[:10])
        
        print(f"\nBIZCOND_CUSTODY_ND_WAREHS_NM (Not None Count: {len(biz_samples)}):")
        print(biz_samples[:10])
        
        # '업태보관및창고업명'이 '1'로만 나오는지 확인
        unique_biz = set(biz_samples)
        print(f"\nUnique Biz Names: {unique_biz}")

        
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    check_specific_fields()
