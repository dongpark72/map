import requests
from urllib.parse import unquote

service_key = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')
sgg = '26440'
bjd = '10600'
bun = '1576'
ji = '0002'

base_url = "https://apis.data.go.kr/1613000/BldRgstHubService"

print(f"--- Checking Building HUB API for Mieum-dong 1576-2 ---")

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
        print(f"\nEndpoint: {endpoint}")
        print(f"Status: {res.status_code}")
        if "item" in res.text:
            print("FOUND ITEMS!")
            # print(res.text[:500])
        else:
            print("No items.")
    except Exception as e:
        print(f"Error: {e}")

# 총괄표제부 (Total)
check_endpoint("getBrRecapTitleInfo")
# 일반표제부 (Title)
check_endpoint("getBrTitleInfo")
# 층별개요 (Floor)
check_endpoint("getBrFlrInfo")
