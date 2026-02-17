import requests
import urllib.parse
import xml.etree.ElementTree as ET
import re

# 온비드 API 테스트 - 더 많은 샘플 확인
url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"

key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

# 경기도 시흥시로 테스트
sido = "경기도"
sgk = "시흥시"

raw_key = urllib.parse.unquote(key)
query_params = [
    f"serviceKey={raw_key}",
    f"numOfRows=20",  # 20개 확인
    f"pageNo=1",
    f"DPSL_MTD_CD=0001",
    f"SIDO={urllib.parse.quote(sido)}",
    f"SGK={urllib.parse.quote(sgk)}",
    f"CTGR_ID=10000"  # 부동산만
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
                    print(f"Found {len(items)} items\n")
                    
                    # 모든 아이템의 필드 수집
                    all_fields = set()
                    for item in items:
                        for child in item:
                            all_fields.add(child.tag)
                    
                    print("=== All Available Fields ===")
                    for field in sorted(all_fields):
                        print(f"  - {field}")
                    
                    print("\n=== Sample Items ===")
                    for idx, item in enumerate(items[:5], 1):
                        print(f"\n--- Item {idx} ---")
                        
                        def get_v(tag):
                            el = item.find(tag)
                            return el.text.strip() if el is not None and el.text else ''
                        
                        cltr_nm = get_v('CLTR_NM')
                        goods_nm = get_v('GOODS_NM')
                        bid_mnmt_no = get_v('BID_MNMT_NO')
                        pbct_cltr_stat_nm = get_v('PBCT_CLTR_STAT_NM')
                        
                        print(f"물건명: {cltr_nm}")
                        print(f"상태: {pbct_cltr_stat_nm}")
                        print(f"BID_MNMT_NO: {bid_mnmt_no}")
                        print(f"GOODS_NM: {goods_nm}")
                        
                        # GOODS_NM에서 면적 정보 파싱 시도
                        if goods_nm:
                            # 토지 면적 찾기
                            land_match = re.search(r'토지\s*([0-9,.]+)\s*㎡', goods_nm)
                            if land_match:
                                print(f"  -> 토지면적: {land_match.group(1)}㎡")
                            
                            # 건물 면적 찾기
                            bld_match = re.search(r'건물\s*([0-9,.]+)\s*㎡', goods_nm)
                            if bld_match:
                                print(f"  -> 건물면적: {bld_match.group(1)}㎡")
                            
                            # 입찰 회수 찾기
                            bid_match = re.search(r'(\d+)회\s*입찰', goods_nm)
                            if bid_match:
                                print(f"  -> 입찰회수: {bid_match.group(1)}회")
                        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
