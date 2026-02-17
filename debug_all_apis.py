import requests
from urllib.parse import unquote

service_key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
unquoted_key = unquote(service_key)

lawd_cd = '26440'
deal_ym = '202502'

# 1. 아파트 API 테스트
apt_url = 'http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev'
params = {'serviceKey': unquoted_key, 'LAWD_CD': lawd_cd, 'DEAL_YMD': deal_ym}

print("--- Testing APT API ---")
res = requests.get(apt_url, params=params)
print(f"APT Status: {res.status_code}")
if res.status_code == 200:
    print(f"APT Sample: {res.text[:200]}")
else:
    print(f"APT Failed: {res.text[:200]}")

# 2. 토지 API 테스트
land_url = 'https://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade'
print("\n--- Testing LAND API ---")
res = requests.get(land_url, params=params)
print(f"LAND Status: {res.status_code}")
if res.status_code == 200:
    print(f"LAND Sample: {res.text[:200]}")

# 3. 공장 API (다시 시도)
factory_url = 'http://apis.data.go.kr/1613000/RTMSDataSvcNIndTrade/getRTMSDataSvcNIndTrade'
print("\n--- Testing FACTORY API ---")
res = requests.get(factory_url, params=params)
print(f"FACTORY Status: {res.status_code}")
print(f"FACTORY Response: {res.text[:200]}")
