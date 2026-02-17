import requests
from urllib.parse import unquote

# 인코딩된 키를 unquote 처리
service_key = unquote('eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==')

sigungu_cd = '26440'
bjdong_cd = '10600'
bun = '1576'.zfill(4)
ji = '0002'

url = "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo"

params = {
    'serviceKey': service_key,
    'sigunguCd': sigungu_cd,
    'bjdongCd': bjdong_cd,
    'platGbCd': '0',
    'bun': bun,
    'ji': ji,
    'numOfRows': 10
}

print(f"Testing with Unquoted Key and zfilled bun/ji...")
res = requests.get(url, params=params)
print(f"Status: {res.status_code}")
print(f"Response: {res.text[:1000]}")
