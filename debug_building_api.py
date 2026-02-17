import requests
import xml.etree.ElementTree as ET

service_key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
sigungu_cd = '26440' # 부산 강서구
bjdong_cd = '10600'  # 미음동
bun = '1576'.zfill(4)
ji = '2'.zfill(4)

url = "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo"

def test_api(plat_gb):
    params = {
        'serviceKey': service_key,
        'sigunguCd': sigungu_cd,
        'bjdongCd': bjdong_cd,
        'platGbCd': plat_gb,
        'bun': bun,
        'ji': ji,
        'numOfRows': 10
    }
    print(f"\nTesting with platGbCd={plat_gb}...")
    try:
        res = requests.get(url, params=params, timeout=10)
        print(f"Status: {res.status_code}")
        if "item" in res.text:
            print("SUCCESS: Data found!")
            print(res.text[:500])
        else:
            print("FAILED: No items found.")
            print(res.text[:300])
    except Exception as e:
        print(f"Error: {e}")

test_api('0') # 일반
test_api('1') # 산
test_api('2') # 가번지
