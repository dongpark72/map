"""
카카오 지도 API로 주소 → PNU 변환
"""
import requests

# 여러 형식으로 시도
addresses = [
    "부산 동남로71길 41",
    "부산광역시 동남로71길 41",
    "부산 수영구 동남로71길 41",
    "부산광역시 수영구 동남로71길 41",
]

# 카카오 REST API 키
KAKAO_REST_API_KEY = "0d9c2e2988d5b30dc525d0ef29f2c362"

# 주소 검색
url = "https://dapi.kakao.com/v2/local/search/address.json"
headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}

found = False
for address in addresses:
    print(f"시도 중: {address}")
    params = {"query": address}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if data.get('documents'):
        found = True
        doc = data['documents'][0]
        
        print(f"\n✓ 주소 찾음: {address}")
        print("=" * 80)
        print(f"도로명주소: {doc.get('road_address', {}).get('address_name', 'N/A') if doc.get('road_address') else 'N/A'}")
        print(f"지번주소: {doc.get('address', {}).get('address_name', 'N/A') if doc.get('address') else 'N/A'}")
        
        # PNU 정보
        if 'address' in doc and doc['address']:
            addr = doc['address']
            
            # PNU 구성
            b_code = addr.get('b_code', '')  # 법정동코드 (10자리)
            mountain_yn = addr.get('mountain_yn', 'N')
            main_address_no = addr.get('main_address_no', '')
            sub_address_no = addr.get('sub_address_no', '')
            
            # 대지구분: N=대지(1), Y=산(2)
            land_type = '1' if mountain_yn == 'N' else '2'
            
            # PNU 생성 (19자리)
            pnu = f"{b_code}{land_type}{str(main_address_no).zfill(4)}{str(sub_address_no).zfill(4)}"
            
            print(f"\nPNU: {pnu}")
            print(f"  - 법정동코드: {b_code}")
            print(f"  - 대지구분: {land_type} ({'대지' if land_type == '1' else '산'})")
            print(f"  - 본번: {str(main_address_no).zfill(4)}")
            print(f"  - 부번: {str(sub_address_no).zfill(4)}")
            
            # 파싱
            sigungu = pnu[0:5]
            bjdong = pnu[5:10]
            platGb = '0' if pnu[10] == '1' else '1'
            bun = pnu[11:15]
            ji = pnu[15:19]
            
            print(f"\nAPI 파라미터:")
            print(f"  - sigunguCd: {sigungu}")
            print(f"  - bjdongCd: {bjdong}")
            print(f"  - platGbCd: {platGb}")
            print(f"  - bun: {bun}")
            print(f"  - ji: {ji}")
            
            # 테스트 URL 저장
            with open('test_address_pnu.txt', 'w', encoding='utf-8') as f:
                f.write(f"주소: {address}\n")
                f.write(f"PNU: {pnu}\n")
                f.write(f"sigungu={sigungu}, bjdong={bjdong}, platGb={platGb}, bun={bun}, ji={ji}\n")
            
            print("\n✓ test_address_pnu.txt 파일에 저장되었습니다.")
        else:
            print("\n⚠️ PNU 정보를 찾을 수 없습니다.")
        break

if not found:
    print(f"\n❌ 모든 주소 형식으로 검색했지만 찾을 수 없습니다.")
