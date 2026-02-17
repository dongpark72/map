import requests
import urllib.parse
import json

KEY_BASE64 = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
URL_V2 = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

def test_v2_encoding_swaps():
    print(f"Targeting: {URL_V2}")
    
    # Case 1: Decoded Key (Raw bytes -> URL Encode by requests)
    # requests params에 넣으면 requests가 알아서 인코딩함.
    # 하지만 Base64 키 자체에 %문자가 없어서 그대로 날아감. -> '+'가 ' ' 공백으로 변환될 위험 있음.
    # 따라서 urllib.parse.quote를 명시적으로 해주는게 안전.
    
    encoded_key = urllib.parse.quote(KEY_BASE64)
    double_encoded_key = urllib.parse.quote(encoded_key)
    
    cases = [
        ("Single Encoded", encoded_key),
        ("Double Encoded", double_encoded_key),
        ("Raw Key (Let requests handle)", KEY_BASE64)
    ]
    
    for label, key_val in cases:
        print(f"\n--- {label} ---")
        
        # 수동 URL 구성 (requests 간섭 배제)
        if label != "Raw Key (Let requests handle)":
            full_url = f"{URL_V2}?ServiceKey={key_val}&pageNo=1&numOfRows=1&_type=json"
            try:
                res = requests.get(full_url, timeout=5)
                print(f"Status: {res.status_code}")
                print(f"Body: {res.text[:500]}") # 에러 메시지 확인 중요
            except Exception as e:
                print(e)
        else:
            # requests param 이용
            try:
                res = requests.get(URL_V2, params={'ServiceKey': key_val, 'pageNo': 1, 'numOfRows': 1, '_type': 'json'}, timeout=5)
                print(f"Status: {res.status_code}")
                print(f"Body: {res.text[:500]}")
            except Exception as e:
                print(e)

if __name__ == "__main__":
    test_v2_encoding_swaps()
