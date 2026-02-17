import requests
from urllib.parse import unquote

service_key = unquote('eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==')

# 규격 A: (현재 사용중인 규격) sigunguCd, bjdongCd
# 규격 B: sigungu_cd, bjdong_cd
# 규격 C: sgg_cd, bjd_cd

url = "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo"

def try_params(name, p):
    p['serviceKey'] = service_key
    print(f"\n--- Testing {name} ---")
    try:
        res = requests.get(url, params=p, timeout=5)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:200]}")
    except: pass

# 규격 A
try_params("A (sigunguCd)", {'sigunguCd': '26440', 'bjdongCd': '10600', 'platGbCd': '0', 'bun': '1576', 'ji': '0002'})

# 규격 B (Snake Case)
try_params("B (sigungu_cd)", {'sigungu_cd': '26440', 'bjdong_cd': '10600', 'plat_gb_cd': '0', 'bun': '1576', 'ji': '0002'})

# 규격 C (Short)
try_params("C (sgg_cd)", {'sgg_cd': '26440', 'bjd_cd': '10600', 'bun': '1576', 'ji': '0002'})
