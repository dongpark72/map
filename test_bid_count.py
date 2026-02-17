import requests
import urllib.parse
import xml.etree.ElementTree as ET
import re

url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

# 서울시로 테스트
sido = "서울특별시"
sgk = "구로구"

raw_key = urllib.parse.unquote(key)
query_params = [
    f"serviceKey={raw_key}",
    f"numOfRows=20",
    f"pageNo=1",
    f"DPSL_MTD_CD=0001",
    f"SIDO={urllib.parse.quote(sido)}",
    f"SGK={urllib.parse.quote(sgk)}",
    f"CTGR_ID=10000"
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
                    
                    for idx, item in enumerate(items[:10], 1):
                        def get_v(tag):
                            el = item.find(tag)
                            return el.text.strip() if el is not None and el.text else ''
                        
                        cltr_nm = get_v('CLTR_NM')
                        pbct_cltr_stat_nm = get_v('PBCT_CLTR_STAT_NM')
                        bid_prgn_nft = get_v('BID_PRGN_NFT')
                        bid_mnmt_no = get_v('BID_MNMT_NO')
                        goods_nm = get_v('GOODS_NM')
                        ctgr_full_nm = get_v('CTGR_FULL_NM')
                        
                        print(f"--- Item {idx} ---")
                        print(f"물건명: {cltr_nm}")
                        print(f"상태: {pbct_cltr_stat_nm}")
                        print(f"종류: {ctgr_full_nm}")
                        print(f"BID_PRGN_NFT: '{bid_prgn_nft}'")
                        print(f"BID_MNMT_NO: '{bid_mnmt_no}'")
                        
                        # GOODS_NM에서 입찰 회수 찾기
                        if goods_nm:
                            # 다양한 패턴 시도
                            patterns = [
                                r'(\d+)회\s*입찰',
                                r'입찰\s*(\d+)회',
                                r'(\d+)회차',
                                r'(\d+)차\s*입찰',
                                r'유찰\s*(\d+)회',
                                r'(\d+)회\s*유찰'
                            ]
                            
                            found = False
                            for pattern in patterns:
                                match = re.search(pattern, goods_nm)
                                if match:
                                    print(f"  -> GOODS_NM에서 발견: {match.group(1)}회 (패턴: {pattern})")
                                    found = True
                                    break
                            
                            if not found:
                                # GOODS_NM 일부 출력 (처음 200자)
                                print(f"  -> GOODS_NM (일부): {goods_nm[:200]}")
                        
                        print()
                    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
