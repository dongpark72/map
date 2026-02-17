import requests
from urllib.parse import unquote

# 2번 키 (공장 API에서 성공했던 키)
service_key = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')

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

print(f"Testing Building API with KEY 2...")
res = requests.get(url, params=params)
print(f"Status: {res.status_code}")
print(f"Response: {res.text[:1000]}")
