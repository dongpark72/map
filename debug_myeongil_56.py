import requests
from urllib.parse import unquote

service_key = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')
sgg = '11740'
bjd = '10900'
bun = '0056'
ji = '0000'

base_url = "https://apis.data.go.kr/1613000/BldRgstHubService"

def check(endpoint, b, j):
    url = f"{base_url}/{endpoint}"
    params = {
        'serviceKey': service_key,
        'sigunguCd': sgg,
        'bjdongCd': bjd,
        'platGbCd': '0',
        'bun': b,
        'ji': j,
        'numOfRows': 10
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if "<item>" in res.text:
            print(f"[FOUND] {endpoint} with {b}-{j}")
            return True
        else:
            print(f"[EMPTY] {endpoint} with {b}-{j}")
            return False
    except Exception as e:
        print(f"[ERROR] {endpoint}: {e}")
        return False

print("--- Debugging Myeongil-dong 56 ---")
check("getBrRecapTitleInfo", "0056", "0000")
check("getBrTitleInfo", "0056", "0000")

# If empty, try without padding just in case
check("getBrTitleInfo", "56", "0")
