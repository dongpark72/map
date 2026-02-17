import requests
from urllib.parse import unquote

service_key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
unquoted_key = unquote(service_key)

lawd_cd = '26440'
deal_ym = '202502'

# 1. 공장및창고 Dev API 테스트
factory_dev_url = 'http://apis.data.go.kr/1613000/RTMSDataSvcNIndTradeDev/getRTMSDataSvcNIndTradeDev'
params_camel = {'serviceKey': unquoted_key, 'lawdCd': lawd_cd, 'dealYmd': deal_ym}

print("--- Testing FACTORY DEV API (lawdCd/dealYmd) ---")
try:
    res = requests.get(factory_dev_url, params=params_camel, timeout=10)
    print(f"FACTORY DEV Status: {res.status_code}")
    print(f"FACTORY DEV Response: {res.text[:500]}")
    
    if res.status_code == 200:
        print("\nSUCCESS! Factory Dev API works.")
except Exception as e:
    print(f"Error: {e}")

# 2. 공장및창고 Dev API 테스트 (LAWD_CD/DEAL_YMD)
params_upper = {'serviceKey': unquoted_key, 'LAWD_CD': lawd_cd, 'DEAL_YMD': deal_ym}
print("\n--- Testing FACTORY DEV API (LAWD_CD/DEAL_YMD) ---")
try:
    res = requests.get(factory_dev_url, params=params_upper, timeout=10)
    print(f"FACTORY DEV (Upper) Status: {res.status_code}")
    print(f"FACTORY DEV (Upper) Response: {res.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
