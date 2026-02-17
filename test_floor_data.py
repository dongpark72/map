"""
Test script to verify floor data retrieval from building_detail_proxy
"""
import requests
import xml.etree.ElementTree as ET
import urllib.parse

# Test PNU from the uploaded image (영도구 동삼동 318-49)
# 부산광역시 영도구 = 2644010400
# 동삼동 법정동코드 = 10400
test_pnu = "2644010400103180049"

print(f"Testing PNU: {test_pnu}")
print("=" * 80)

# Alternative PNU
alt_pnu = "2644010100103180049"

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"

api_url_recap = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
api_url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
api_url_basis = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrBasisOulnInfo"
api_url_flr = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
api_url_expos = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrExposPubuseAreaInfo"

keys_to_try = [
    "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
    "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368",
]

for pnu in [test_pnu, alt_pnu]:
    print(f"\n\nTrying PNU: {pnu}")
    print("-" * 80)
    
    sigungu = pnu[0:5]
    bjdong = pnu[5:10]
    platGb = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15])).zfill(4)
    ji = str(int(pnu[15:19])).zfill(4)
    
    print(f"Parsed: sigungu={sigungu}, bjdong={bjdong}, platGb={platGb}, bun={bun}, ji={ji}")
    
    for key_idx, key in enumerate(keys_to_try):
        print(f"\n  Using API Key #{key_idx + 1}")
        enc_key = urllib.parse.quote(key)
        
        # Try Title API
        print(f"\n  [1] getBrTitleInfo (일반표제부)")
        try:
            q = f"{api_url_title}^serviceKey={enc_key}|numOfRows=100|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
            res = session.get(connector_url, params={'url': q}, timeout=6)
            if res.status_code == 200 and "<item>" in res.text:
                items = ET.fromstring(res.text).findall('.//item')
                print(f"    ✓ Found {len(items)} items")
                for idx, item in enumerate(items):
                    pk = item.find('mgmBldrgstPk')
                    bldNm = item.find('bldNm')
                    totArea = item.find('totArea')
                    print(f"      Item {idx+1}: PK={pk.text if pk is not None else 'N/A'}, "
                          f"건물명={bldNm.text if bldNm is not None else 'N/A'}, "
                          f"연면적={totArea.text if totArea is not None else 'N/A'}")
                    
                    # Try to get floor info for this PK
                    if pk is not None and pk.text:
                        print(f"\n      Testing floor data for PK: {pk.text}")
                        
                        # Try getBrFlrOulnInfo
                        try:
                            q_flr = f"{api_url_flr}^serviceKey={enc_key}|numOfRows=300|mgmBldrgstPk={pk.text}"
                            res_flr = session.get(connector_url, params={'url': q_flr}, timeout=5)
                            if res_flr.status_code == 200 and "<item>" in res_flr.text:
                                flr_items = ET.fromstring(res_flr.text).findall('.//item')
                                print(f"        ✓ getBrFlrOulnInfo: Found {len(flr_items)} floor records")
                                for f_idx, f_item in enumerate(flr_items[:3]):  # Show first 3
                                    flrGb = f_item.find('flrGbCdNm')
                                    flrNo = f_item.find('flrNoNm')
                                    area = f_item.find('area')
                                    purps = f_item.find('mainPurpsCdNm')
                                    print(f"          Floor {f_idx+1}: {flrGb.text if flrGb is not None else ''} "
                                          f"{flrNo.text if flrNo is not None else ''}, "
                                          f"용도={purps.text if purps is not None else ''}, "
                                          f"면적={area.text if area is not None else ''}")
                            else:
                                print(f"        ✗ getBrFlrOulnInfo: No data")
                        except Exception as e:
                            print(f"        ✗ getBrFlrOulnInfo error: {e}")
                        
                        # Try getBrExposPubuseAreaInfo
                        try:
                            q_exp = f"{api_url_expos}^serviceKey={enc_key}|numOfRows=300|mgmBldrgstPk={pk.text}"
                            res_exp = session.get(connector_url, params={'url': q_exp}, timeout=5)
                            if res_exp.status_code == 200 and "<item>" in res_exp.text:
                                exp_items = ET.fromstring(res_exp.text).findall('.//item')
                                print(f"        ✓ getBrExposPubuseAreaInfo: Found {len(exp_items)} records")
                            else:
                                print(f"        ✗ getBrExposPubuseAreaInfo: No data")
                        except Exception as e:
                            print(f"        ✗ getBrExposPubuseAreaInfo error: {e}")
            else:
                print(f"    ✗ No items found (status={res.status_code})")
        except Exception as e:
            print(f"    ✗ Error: {e}")
        
        # Try Basis API
        print(f"\n  [2] getBrBasisOulnInfo (기본개요)")
        try:
            q = f"{api_url_basis}^serviceKey={enc_key}|numOfRows=100|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
            res = session.get(connector_url, params={'url': q}, timeout=6)
            if res.status_code == 200 and "<item>" in res.text:
                items = ET.fromstring(res.text).findall('.//item')
                print(f"    ✓ Found {len(items)} items")
                for idx, item in enumerate(items):
                    pk = item.find('mgmBldrgstPk')
                    totArea = item.find('totArea')
                    print(f"      Item {idx+1}: PK={pk.text if pk is not None else 'N/A'}, "
                          f"연면적={totArea.text if totArea is not None else 'N/A'}")
            else:
                print(f"    ✗ No items found")
        except Exception as e:
            print(f"    ✗ Error: {e}")
        
        # Try Recap API
        print(f"\n  [3] getBrRecapTitleInfo (총괄표제부)")
        try:
            q = f"{api_url_recap}^serviceKey={enc_key}|numOfRows=100|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
            res = session.get(connector_url, params={'url': q}, timeout=6)
            if res.status_code == 200 and "<item>" in res.text:
                items = ET.fromstring(res.text).findall('.//item')
                print(f"    ✓ Found {len(items)} items")
                for idx, item in enumerate(items):
                    pk = item.find('mgmBldrgstPk')
                    totArea = item.find('totArea')
                    print(f"      Item {idx+1}: PK={pk.text if pk is not None else 'N/A'}, "
                          f"연면적={totArea.text if totArea is not None else 'N/A'}")
            else:
                print(f"    ✗ No items found")
        except Exception as e:
            print(f"    ✗ Error: {e}")

print("\n\n" + "=" * 80)
print("Test complete!")
