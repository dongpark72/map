import requests
from urllib.parse import unquote

service_key = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')
sgg = '26440'
bjd = '10600'
bun = '1576'
ji = '0002'

base_url = "https://apis.data.go.kr/1613000/BldRgstHubService"

def check_endpoint(endpoint):
    url = f"{base_url}/{endpoint}"
    params = {
        'serviceKey': service_key,
        'sigunguCd': sgg,
        'bjdongCd': bjd,
        'platGbCd': '0',
        'bun': bun,
        'ji': ji,
        'numOfRows': 10
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        # Check for actual item tags, not just the container <items>
        if "<item>" in res.text:
            print(f"[FOUND] {endpoint}")
        else:
            print(f"[EMPTY] {endpoint}")
    except Exception as e:
        print(f"[ERROR] {endpoint}: {e}")

check_endpoint("getBrRecapTitleInfo")
check_endpoint("getBrTitleInfo")
check_endpoint("getBrFlrInfo")

# Also check without padding for Ji
def check_no_padding(endpoint):
    url = f"{base_url}/{endpoint}"
    params = {
        'serviceKey': service_key,
        'sigunguCd': sgg,
        'bjdongCd': bjd,
        'platGbCd': '0',
        'bun': bun,
        'ji': '2', # NO PADDING
        'numOfRows': 10
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if "<item>" in res.text:
            print(f"[FOUND NO PADDING] {endpoint}")
        else:
            print(f"[EMPTY NO PADDING] {endpoint}")
    except: pass

check_no_padding("getBrRecapTitleInfo")
check_no_padding("getBrTitleInfo")
