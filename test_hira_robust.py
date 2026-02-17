import requests
import urllib.parse
import time

# 키 정의
KEY_BASE64 = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
KEY_HEX = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

# URL (HTTPS 시도)
URL = "https://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/xml, */*'
}

def test_robust(key, desc):
    print(f"\n>>>> Testing {desc} <<<<")
    
    # 1. 인코딩하여 전송 (서비스키는 대문자 ServiceKey로 시도 - 이미지 참조)
    encoded_key = urllib.parse.quote(key)
    
    # 파라미터 조합
    params_str = f"ServiceKey={encoded_key}&pageNo=1&numOfRows=1&_type=json"
    full_url = f"{URL}?{params_str}"
    
    print(f"Target URL: {full_url}")
    
    try:
        # verify=False는 SSL 인증서 문제 무시 (개발 편의)
        res = requests.get(full_url, headers=HEADERS, verify=False, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Content-Type: {res.headers.get('Content-Type')}")
        print(f"Body First 500: {res.text[:500]}")
        
    except Exception as e:
        print(f"EXCEPTION: {e}")

print("--- Starting Robust Test ---")

# Test 1: Base64 Key
test_robust(KEY_BASE64, "Base64 Key (Decoding Key -> Encoded)")

# Test 2: Hex Key
test_robust(KEY_HEX, "Hex Key (Assuming it is a key)")
