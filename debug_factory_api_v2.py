import requests
from urllib.parse import unquote

# 이미 인코딩된 키인 경우 unquote로 원래 키를 얻음
raw_key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
unquoted_key = unquote(raw_key)

lawd_cd = '26440'
deal_ym = '202502'

# 공장 및 창고 API 엔드포인트
url = 'http://apis.data.go.kr/1613000/RTMSDataSvcNIndTrade/getRTMSDataSvcNIndTrade'

# 인코딩이 안 된 순수한 파라미터 딕셔너리
params = {
    'serviceKey': unquoted_key,
    'LAWD_CD': lawd_cd,
    'DEAL_YMD': deal_ym,
    'numOfRows': 10,
    'pageNo': 1
}

print(f"Testing with LAWD_CD / DEAL_YMD and Unquoted Key...")
try:
    # requests가 파라미터를 자동으로 인코딩하도록 함
    res = requests.get(url, params=params, timeout=10)
    print(f"Status: {res.status_code}")
    if "Unexpected errors" in res.text:
        print("Still failing with LAWD_CD. Retrying with lawdCd/dealYmd...")
        params_camel = {
            'serviceKey': unquoted_key,
            'lawdCd': lawd_cd,
            'dealYmd': deal_ym,
        }
        res = requests.get(url, params=params_camel, timeout=10)
        print(f"Status (Camel): {res.status_code}")
        
    print(f"Response: {res.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
