import requests
from urllib.parse import unquote

service_key = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')
sigungu_cd = '26440'
bjdong_cd = '10600'
bun = '1576'
ji = '2'

# Hub 서비스 엔드포인트 + 기본 기능명
url = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

params = {
    'serviceKey': service_key,
    'sigunguCd': sigungu_cd,
    'bjdongCd': bjdong_cd,
    'platGbCd': '0',
    'bun': bun.zfill(4),
    'ji': ji.zfill(4),
    'numOfRows': 10
}

print(f"Testing Building HUB API (Default Name)...")
res = requests.get(url, params=params)
print(f"Status: {res.status_code}")
print(f"Response: {res.text[:500]}")
