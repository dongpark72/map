import requests
from urllib.parse import unquote

key1 = unquote('eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==')
key2 = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')

sgg = '11740'
bjd = '10900'
bun = '0056'
ji = '0000'

def test(url, key, name):
    params = {
        'serviceKey': key,
        'sigunguCd': sgg,
        'bjdongCd': bjd,
        'platGbCd': '0',
        'bun': bun,
        'ji': ji,
        'numOfRows': 10
    }
    try:
        res = requests.get(url, params=params, timeout=5)
        if "<item>" in res.text:
            print(f"[SUCCESS] {name}")
        else:
            print(f"[EMPTY] {name}")
    except:
        print(f"[ERROR] {name}")

print("--- Testing Version 2 Service with both keys ---")
v2_url = "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo"
test(v2_url, key1, "V2 - Key 1")
test(v2_url, key2, "V2 - Key 2")

print("\n--- Testing Hub Service with Key 1 ---")
hub_url = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
test(hub_url, key1, "Hub - Key 1")
