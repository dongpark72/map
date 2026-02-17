import requests
from urllib.parse import unquote

# 2번 키
service_key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
unquoted_key = unquote(service_key)

lawd_cd = '26440'
deal_ym = '202502'
url = 'https://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'

params = {'serviceKey': unquoted_key, 'LAWD_CD': lawd_cd, 'DEAL_YMD': deal_ym}

print(f"Testing with KEY 2...")
res = requests.get(url, params=params, timeout=10)
print(f"Status: {res.status_code}")
print(f"Response: {res.text[:500]}")
