import requests
from urllib.parse import unquote

service_key = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')
sgg = '26440'
bjd = '10600'
url = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

def test_combination(bun, ji, plat='0'):
    params = {
        'serviceKey': service_key,
        'sigunguCd': sgg,
        'bjdongCd': bjd,
        'platGbCd': plat,
        'bun': bun,
        'ji': ji,
        'numOfRows': 5
    }
    try:
        res = requests.get(url, params=params, timeout=5)
        if "item" in res.text:
            print(f"[SUCCESS] bun={bun}, ji={ji}, plat={plat} -> FOUND DATA")
            return True
        else:
            print(f"[EMPTY] bun={bun}, ji={ji}, plat={plat}")
            return False
    except:
        return False

print("--- Testing Mieum-dong 1576-2 Combinations ---")

# 1. 패딩 있음 (기존 방식)
test_combination('1576', '0002')

# 2. 패딩 없음 (가장 유력)
test_combination('1576', '2')

# 3. 호수 없이 (단독 건물인 경우)
test_combination('1576', '0')
test_combination('1576', '')

# 4. 산 번지인 경우
test_combination('1576', '0002', '1')
test_combination('1576', '2', '1')
