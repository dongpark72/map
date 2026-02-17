import requests
import xml.etree.ElementTree as ET

# 부산광역시 사상구 덕포동 369-9
pnu = "2653010400103690009"

print(f"Testing different APIs for PNU: {pnu}")
print(f"Address: 부산광역시 사상구 덕포동 369-9")
print("=" * 80)

# PNU 분해
sigungu = pnu[0:5]
bjdong = pnu[5:10]
platGb = '0' if pnu[10] == '1' else '1'
bun = str(int(pnu[11:15]))
ji = str(int(pnu[15:19]))

print(f"sigunguCd: {sigungu}")
print(f"bjdongCd: {bjdong}")
print(f"platGbCd: {platGb}")
print(f"bun: {bun}")
print(f"ji: {ji}")

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

# 다양한 API 시도
apis = [
    ("getBrTitleInfo", "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"),
    ("getBrRecapTitleInfo", "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"),
]

for api_name, api_url in apis:
    print(f"\n{'=' * 80}")
    print(f"Testing API: {api_name}")
    print(f"URL: {api_url}")
    print("-" * 80)
    
    # 시도 1: 앞자리 0 제거
    print(f"\nAttempt 1: bun={bun}, ji={ji}")
    q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=100"
    
    try:
        res = requests.get(connector_url, params={'url': q}, timeout=10)
        if res.status_code == 200 and '<response>' in res.text:
            root = ET.fromstring(res.text)
            
            # 에러 체크
            result_code = root.find('.//resultCode')
            result_msg = root.find('.//resultMsg')
            if result_code is not None:
                print(f"Result Code: {result_code.text}")
                print(f"Result Message: {result_msg.text if result_msg is not None else 'N/A'}")
            
            items = root.findall('.//item')
            print(f"Found {len(items)} items")
            
            if items:
                for idx, item in enumerate(items, 1):
                    print(f"\n--- Item {idx} ---")
                    for child in item:
                        if child.text and child.text.strip():
                            print(f"{child.tag}: {child.text}")
                continue
        
        # 시도 2: 원본 형식
        bun_orig = pnu[11:15]
        ji_orig = pnu[15:19]
        print(f"\nAttempt 2: bun={bun_orig}, ji={ji_orig}")
        q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun_orig}|ji={ji_orig}|numOfRows=100"
        
        res = requests.get(connector_url, params={'url': q}, timeout=10)
        if res.status_code == 200 and '<response>' in res.text:
            root = ET.fromstring(res.text)
            
            result_code = root.find('.//resultCode')
            result_msg = root.find('.//resultMsg')
            if result_code is not None:
                print(f"Result Code: {result_code.text}")
                print(f"Result Message: {result_msg.text if result_msg is not None else 'N/A'}")
            
            items = root.findall('.//item')
            print(f"Found {len(items)} items")
            
            if items:
                for idx, item in enumerate(items, 1):
                    print(f"\n--- Item {idx} ---")
                    for child in item:
                        if child.text and child.text.strip():
                            print(f"{child.tag}: {child.text}")
        else:
            print(f"No valid response (status: {res.status_code})")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
