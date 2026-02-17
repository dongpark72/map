import requests
import xml.etree.ElementTree as ET

# 부산광역시 강서구 대저1동 790
pnu = "2644011500107900000"

print(f"Testing getBrRecapTitleInfo (총괄표제부) for PNU: {pnu}")
print("=" * 80)

# PNU 분해
sigungu = pnu[0:5]  # 26440
bjdong = pnu[5:10]   # 11500
platGb = '0' if pnu[10] == '1' else '1'  # 0 (대지)
bun = pnu[11:15]     # 0790
ji = pnu[15:19]      # 0000

print(f"sigunguCd: {sigungu}")
print(f"bjdongCd: {bjdong}")
print(f"platGbCd: {platGb}")
print(f"bun (original): {bun}")
print(f"ji (original): {ji}")
print(f"bun (int): {int(bun)}")
print(f"ji (int): {int(ji)}")

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

# 총괄표제부 API
api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"

test_cases = [
    ("With int conversion", str(int(bun)), str(int(ji))),
    ("Original format", bun, ji),
    ("Mixed 1", str(int(bun)), ji),
    ("Mixed 2", bun, str(int(ji))),
]

for test_name, test_bun, test_ji in test_cases:
    print(f"\n{'=' * 80}")
    print(f"Test: {test_name}")
    print(f"bun={test_bun}, ji={test_ji}")
    print("-" * 80)
    
    q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={test_bun}|ji={test_ji}|numOfRows=100"
    
    try:
        res = requests.get(connector_url, params={'url': q}, timeout=10)
        
        if res.status_code == 200 and '<response>' in res.text:
            root = ET.fromstring(res.text)
            
            result_code = root.find('.//resultCode')
            result_msg = root.find('.//resultMsg')
            total_count = root.find('.//totalCount')
            
            print(f"Result Code: {result_code.text if result_code is not None else 'N/A'}")
            print(f"Result Message: {result_msg.text if result_msg is not None else 'N/A'}")
            print(f"Total Count: {total_count.text if total_count is not None else 'N/A'}")
            
            items = root.findall('.//item')
            print(f"Items found: {len(items)}")
            
            if items:
                print(f"\n✓ SUCCESS! Found {len(items)} building(s)")
                for idx, item in enumerate(items, 1):
                    print(f"\n--- Building {idx} ---")
                    # 주요 필드만 출력
                    fields_to_show = ['bldNm', 'dongNm', 'mainPurpsCdNm', 'grndFlrCnt', 'ugrndFlrCnt', 
                                     'totArea', 'archArea', 'platArea', 'vlRat', 'bcRat']
                    for field in fields_to_show:
                        elem = item.find(field)
                        if elem is not None and elem.text:
                            print(f"{field}: {elem.text}")
                
                # 이 케이스가 성공하면 더 이상 테스트하지 않음
                print(f"\n✓ Using this format: bun={test_bun}, ji={test_ji}")
                break
        else:
            print(f"Invalid response (status: {res.status_code})")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
