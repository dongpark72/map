import requests
from urllib.parse import unquote

service_key = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')
url = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

params = {
    'serviceKey': service_key,
    'sigunguCd': '26440',
    'bjdongCd': '10600',
    'platGbCd': '0',
    'bun': '1576',
    'ji': '0002',
    'numOfRows': 1
}

res = requests.get(url, params=params)
print(res.text)
