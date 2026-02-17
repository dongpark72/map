"""
PNU 파싱 로직 테스트
"""

# 테스트 PNU
test_pnu = "2620012100103180045"

print(f"Test PNU: {test_pnu}")
print("=" * 80)

# 현재 로직 (잘못된 것)
sigungu_old = test_pnu[0:5]
bjdong_old = test_pnu[5:10]
platGb_old = '0' if test_pnu[10] == '1' else '1'  # 잘못됨
bun_old = str(int(test_pnu[11:15])).zfill(4)
ji_old = str(int(test_pnu[15:19])).zfill(4)

print("\n[현재 로직 - 잘못됨]")
print(f"  시군구코드: {sigungu_old}")
print(f"  법정동코드: {bjdong_old}")
print(f"  대지구분코드: {platGb_old} (PNU[10]={test_pnu[10]})")
print(f"  번: {bun_old}")
print(f"  지: {ji_old}")

# 올바른 로직
sigungu = test_pnu[0:5]
bjdong = test_pnu[5:10]
pnu_land_type = test_pnu[10]

# PNU 대지구분: 1=대지, 2=산
# API platGbCd: 0=대지, 1=산
if pnu_land_type == '1':
    platGb = '0'  # 대지
elif pnu_land_type == '2':
    platGb = '1'  # 산
else:
    platGb = '0'  # 기본값

bun = str(int(test_pnu[11:15])).zfill(4)
ji = str(int(test_pnu[15:19])).zfill(4)

print("\n[올바른 로직]")
print(f"  시군구코드: {sigungu}")
print(f"  법정동코드: {bjdong}")
print(f"  대지구분코드: {platGb} (PNU[10]={pnu_land_type}, {'대지' if pnu_land_type=='1' else '산' if pnu_land_type=='2' else '기타'})")
print(f"  번: {bun}")
print(f"  지: {ji}")

print("\n" + "=" * 80)
print(f"\n차이점:")
print(f"  대지구분코드: {platGb_old} → {platGb}")
if platGb_old != platGb:
    print(f"  ⚠️ 대지구분코드가 잘못되어 API 조회 실패 가능!")
else:
    print(f"  ✓ 대지구분코드 동일")
