import requests
import urllib.parse
import json

# 사용자 키
KEY = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='

# 새로운 v2 엔드포인트 후보들
V2_URLS = [
    "https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList",
    "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList",  # http 시도
]

def test_v2_endpoint():
    print("--- Testing HIRA API v2 Endpoint ---")
    
    encoded_key = urllib.parse.quote(KEY)
    
    for url in V2_URLS:
        print(f"\nTarget URL: {url}")
        
        # 파라미터: v2도 v1과 유사할 것으로 가정 (pageNo, numOfRows, _type, ServiceKey)
        params_str = f"ServiceKey={encoded_key}&pageNo=1&numOfRows=1&_type=json"
        
        # 병원명 파라미터도 추가해볼 수 있으나, 일단 빈 목록이라도 뜨는지 확인 (전체 조회)
        full_url = f"{url}?{params_str}"
        
        try:
            # verify=False: SSL 인증서 문제 회피
            res = requests.get(full_url, verify=False, timeout=10)
            
            print(f"Status: {res.status_code}")
            print(f"Body: {res.text[:400]}")
            
            if res.status_code == 200:
                if "resultCode" in res.text:
                   print(">>> LOOKS LIKE A VALID API RESPONSE!")
                   
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_v2_endpoint()
