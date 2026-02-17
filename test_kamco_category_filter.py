import requests
import urllib.parse
import xml.etree.ElementTree as ET

url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

sido = "경기도"
sgk = "시흥시"

raw_key = urllib.parse.unquote(key)
query_params = [
    f"serviceKey={raw_key}",
    f"numOfRows=30",
    f"pageNo=1",
    f"DPSL_MTD_CD=0001",
    f"SIDO={urllib.parse.quote(sido)}",
    f"SGK={urllib.parse.quote(sgk)}",
    f"CTGR_ID=10000"  # 부동산 카테고리
]

full_url = f"{url}?{'&'.join(query_params)}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/xml,text/xml,*/*',
}

try:
    response = requests.get(full_url, headers=headers, timeout=10, verify=False)
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        header = root.find('header')
        result_code = header.find('resultCode').text if header is not None else ''
        
        if result_code == '00':
            body = root.find('body')
            if body is not None:
                items_node = body.find('items')
                if items_node is not None:
                    items = items_node.findall('item')
                    print(f"Total items: {len(items)}\n")
                    
                    # 물건종류별 분류
                    real_estate = []
                    vehicles = []
                    securities = []
                    machinery = []
                    others = []
                    
                    for item in items:
                        def get_v(tag):
                            el = item.find(tag)
                            return el.text.strip() if el is not None and el.text else ''
                        
                        ctgr_type_nm = get_v('CTGR_TYPE_NM')
                        ctgr_full_nm = get_v('CTGR_FULL_NM')
                        cltr_nm = get_v('CLTR_NM')
                        
                        item_info = {
                            'name': cltr_nm,
                            'type': ctgr_type_nm,
                            'full': ctgr_full_nm
                        }
                        
                        # 분류
                        if '부동산' in ctgr_type_nm or '부동산' in ctgr_full_nm:
                            real_estate.append(item_info)
                        elif '자동차' in ctgr_type_nm or '운송' in ctgr_type_nm:
                            vehicles.append(item_info)
                        elif '증권' in ctgr_type_nm or '과리' in ctgr_type_nm:
                            securities.append(item_info)
                        elif '기계' in ctgr_type_nm or '물품' in ctgr_type_nm:
                            machinery.append(item_info)
                        else:
                            others.append(item_info)
                    
                    print("="*80)
                    print(f"부동산: {len(real_estate)}개")
                    print("="*80)
                    for idx, item in enumerate(real_estate[:5], 1):
                        print(f"{idx}. {item['name']}")
                        print(f"   종류: {item['type']}")
                        print(f"   전체: {item['full']}\n")
                    
                    print("="*80)
                    print(f"자동차/운송장비: {len(vehicles)}개")
                    print("="*80)
                    for idx, item in enumerate(vehicles[:3], 1):
                        print(f"{idx}. {item['name']}")
                        print(f"   종류: {item['type']}")
                        print(f"   전체: {item['full']}\n")
                    
                    print("="*80)
                    print(f"증권/과리: {len(securities)}개")
                    print("="*80)
                    for idx, item in enumerate(securities[:3], 1):
                        print(f"{idx}. {item['name']}")
                        print(f"   종류: {item['type']}")
                        print(f"   전체: {item['full']}\n")
                    
                    print("="*80)
                    print(f"기계/물품: {len(machinery)}개")
                    print("="*80)
                    for idx, item in enumerate(machinery[:3], 1):
                        print(f"{idx}. {item['name']}")
                        print(f"   종류: {item['type']}")
                        print(f"   전체: {item['full']}\n")
                    
                    if others:
                        print("="*80)
                        print(f"기타: {len(others)}개")
                        print("="*80)
                        for idx, item in enumerate(others[:3], 1):
                            print(f"{idx}. {item['name']}")
                            print(f"   종류: {item['type']}")
                            print(f"   전체: {item['full']}\n")
                    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
