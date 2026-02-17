import requests
import urllib.parse
import json

# 저장된 키 목록
KEYS = [
    # Key 1: Base64 포맷 (일반적인 공공데이터포털 키 형식)
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    # Key 2: Hex 포맷 (형식이 다름, 확인 필요)
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

URL = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"

def test_api_call(key_index, key, use_manual_construction=False, do_quote=True):
    explanation = f"Key[{key_index}] | ManualConstruct={use_manual_construction} | DoQuote={do_quote}"
    print(f"\n--- Testing: {explanation} ---")
    
    params = {
        'pageNo': '1',
        'numOfRows': '1',
        '_type': 'json'
    }

    try:
        final_url = URL
        if use_manual_construction:
            # 수동으로 쿼리스트링 구성
            encoded_key = urllib.parse.quote(key) if do_quote else key
            qs_list = [f"{k}={v}" for k, v in params.items()]
            qs_list.append(f"serviceKey={encoded_key}") # serviceKey는 대소문자 주의 (보통 serviceKey 또는 ServiceKey)
            
            # API 문서(이미지)에는 'ServiceKey'라고 되어있는 예시도 있고 'serviceKey'도 있음. 둘 다 시도해보거나 표준을 따름.
            # 하지만 보통 공공데이터포털은 대소문자 구분함. 이미지 예시 1)에는 'getHospBasisList1? ...' 식으로 되어있고 파라미터는 안보임.
            # 이미지 예시 2)에는 'ServiceKey=...' 라고 되어있음.
            # 일단 'ServiceKey'와 'serviceKey' 둘 다 테스트 해보는게 좋겠으나, 우선 'serviceKey'로 시도 (일반적 관례)
            
            # 이미지 2번째 장: String ServiceKey = ... 
            # URL 예시: ...&ServiceKey=ServiceKey...
            # 따라서 'ServiceKey' 대문자 S가 맞을 수도 있음. 
            # 공공데이터포털 표준은 보통 serviceKey이지만, HIRA 상세 가이드를 따름.
            
            qs = "&".join(qs_list)
            final_url = f"{URL}?{qs}"
            
            print(f"Request URL: {final_url}")
            res = requests.get(final_url, timeout=10)
        else:
            # requests params 이용
            # 여기서는 키를 그대로 넣음 (requests가 알아서 인코딩)
            req_params = params.copy()
            req_params['serviceKey'] = key # 소문자 s 시도
            
            print(f"Request with params: {req_params}")
            res = requests.get(URL, params=req_params, timeout=10)
            print(f"Generated URL: {res.url}")

        print(f"Status Code: {res.status_code}")
        print(f"Response Body: {res.text[:500]}")
        
        # 성공 판별
        if res.status_code == 200 and '<resultCode>00</resultCode>' in res.text:
             print(">>> SUCCESS: XML Success Response Found")
        elif res.status_code == 200 and '"resultCode":"00"' in res.text:
             print(">>> SUCCESS: JSON Success Response Found")
             
    except Exception as e:
        print(f"Error: {e}")

# 실행
print("Starting Tests for getHospBasisList1...")

# 테스트 1: Key 1 (Base64) - requests params 이용 (자동 인코딩)
test_api_call(0, KEYS[0], use_manual_construction=False)

# 테스트 2: Key 1 (Base64) - 수동 구성, 인코딩 수행 (이미지 가이드 준수) & 파라미터명 'ServiceKey' (대문자)
# 이미지를 보면 'ServiceKey' 파라미터명을 쓰는 예시가 있음.
def test_manual_key_name(key, key_name='serviceKey'):
    print(f"\n--- Testing Manual with Key Name: {key_name} ---")
    params = "&pageNo=1&numOfRows=1&_type=json"
    encoded_key = urllib.parse.quote(key)
    full_url = f"{URL}?{key_name}={encoded_key}{params}"
    print(f"URL: {full_url}")
    try:
        res = requests.get(full_url, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text[:300]}")
    except Exception as e:
        print(f"Error: {e}")

test_manual_key_name(KEYS[0], 'serviceKey')
test_manual_key_name(KEYS[0], 'ServiceKey') # 대문자 시도

# 테스트 3: Key 1 (Base64) - 인코딩 안하고 보내기 (혹시 이미 인코딩된 키라고 가정?) -> Base64라 /가 있어서 인코딩 안하면 URL 깨짐. 패스.
# 대신 Unquote 한 번 하고 다시 인코딩? 아니면 Unquote된 상태라고 가정?
# 현재 키에 '%'가 없으므로 Unquote는 의미 없음.

# 테스트 4: Key 2 (Hex) - requests params
test_api_call(1, KEYS[1], use_manual_construction=False)

# 테스트 5: Key 2 (Hex) - 수동 구성 ServiceKey
test_manual_key_name(KEYS[1], 'ServiceKey')
