import requests
import urllib.parse
import xml.etree.ElementTree as ET

# 온비드 API 테스트
url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"

KEYS = [
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368',
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
]

# 경기도 시흥시로 테스트
sido = "경기도"
sgk = "시흥시"
page = 1

for key_idx, key in enumerate(KEYS):
    print(f"\n{'='*80}")
    print(f"Testing with KEY {key_idx + 1}")
    print(f"{'='*80}")
    
    raw_key = urllib.parse.unquote(key)
    query_params = [
        f"serviceKey={raw_key}",
        f"numOfRows=5",  # 5개만 테스트
        f"pageNo={page}",
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
            print(f"\n[OK] Response received (status 200)")
            
            # XML 파싱
            root = ET.fromstring(response.text)
            header = root.find('header')
            result_code = header.find('resultCode').text if header is not None else ''
            result_msg = header.find('resultMsg').text if header is not None else ''
            
            print(f"Result Code: {result_code}")
            print(f"Result Message: {result_msg}")
            
            if result_code == '00':
                body = root.find('body')
                if body is not None:
                    items_node = body.find('items')
                    if items_node is not None:
                        items = items_node.findall('item')
                        print(f"\nFound {len(items)} items")
                        
                        for idx, item in enumerate(items[:2], 1):  # 처음 2개만 상세 출력
                            print(f"\n--- Item {idx} ---")
                            
                            # 모든 필드 출력
                            for child in item:
                                tag = child.tag
                                text = child.text.strip() if child.text else ''
                                if text:  # 값이 있는 것만 출력
                                    print(f"{tag}: {text}")
                        
                        # 성공하면 다음 키 테스트 안 함
                        break
            else:
                print(f"[ERROR] API returned error code: {result_code}")
        else:
            print(f"[ERROR] HTTP Status: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] {e}")

print("\n" + "="*80)
print("Test completed")
