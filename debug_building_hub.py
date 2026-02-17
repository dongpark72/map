import requests
from urllib.parse import unquote

# 이미지에 표시된 2번 키
service_key = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')

sigungu_cd = '26440'
bjdong_cd = '10600'
bun = '1576'.zfill(4)
ji = '0002'

# 이미지에 나온 새로운 엔드포인트 (Hub 서비스)
url = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfoHub"

params = {
    'serviceKey': service_key,
    'sigunguCd': sigungu_cd,
    'bjdongCd': bjdong_cd,
    'platGbCd': '0',
    'bun': bun,
    'ji': ji,
    'numOfRows': 10
}

print(f"Testing Building HUB API with KEY 2...")
try:
    res = requests.get(url, params=params, timeout=10)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:1000]}")
    if "item" in res.text:
        print("\nSUCCESS: Building HUB API is working!")
except Exception as e:
    print(f"Error: {e}")
