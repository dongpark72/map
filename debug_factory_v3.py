import requests
from urllib.parse import unquote

service_key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
unquoted_key = unquote(service_key)

lawd_cd = '26440'
deal_ym = '202502'

# 명세서에 나온 정확한 엔드포인트
url = 'https://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'

params = {
    'serviceKey': unquoted_key,
    'LAWD_CD': lawd_cd,
    'DEAL_YMD': deal_ym,
}

print(f"Calling Exact API: {url}")
try:
    res = requests.get(url, params=params, timeout=10)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:1000]}")
except Exception as e:
    print(f"Error: {e}")
