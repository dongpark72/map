
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def test_pnu_detail(pnu):
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    keys = [
        "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
        "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
    ]
    
    sigungu = pnu[:5]
    bjdong = pnu[5:10]
    platGb = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15])).zfill(4)
    ji = str(int(pnu[15:19])).zfill(4)
    
    print(f"PNU: {pnu} -> {sigungu} {bjdong} {platGb} {bun} {ji}")
    
    for key in keys:
        enc_key = urllib.parse.quote(key)
        print(f"\n--- Testing Key: {key[:10]}... ---")
        
        for api in ["getBrTitleInfo", "getBrRecapTitleInfo", "getBrBasisOulnInfo"]:
            url = f"http://apis.data.go.kr/1613000/BldRgstHubService/{api}"
            q = f"{url}^serviceKey={enc_key}|numOfRows=10|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
            try:
                res = requests.get(connector_url, params={'url': q}, timeout=10)
                if "TOTAL_COUNT" in res.text or "<totalCount>" in res.text:
                    root = ET.fromstring(res.text)
                    tc_el = root.find('.//totalCount')
                    tc = tc_el.text if tc_el is not None else "0"
                    items = root.findall('.//item')
                    print(f"API {api}: TotalCount={tc}, ItemsFound={len(items)}")
                    for it in items:
                        pk = it.find('mgmBldrgstPk').text if it.find('mgmBldrgstPk') is not None else "N/A"
                        bld_nm = it.find('bldNm').text if it.find('bldNm') is not None else "N/A"
                        print(f"  - PK: {pk}, Name: {bld_nm}")
                        
                        # Try floors for this PK
                        url_flr = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
                        q_f = f"{url_flr}^serviceKey={enc_key}|numOfRows=100|mgmBldrgstPk={pk}"
                        res_f = requests.get(connector_url, params={'url': q_f}, timeout=10)
                        if "<item>" in res_f.text:
                            root_f = ET.fromstring(res_f.text)
                            floors = root_f.findall('.//item')
                            print(f"    -> Floors Found: {len(floors)}")
                else:
                    print(f"API {api}: No data or error. Response length: {len(res.text)}")
            except Exception as e:
                print(f"API {api} failed: {e}")

if __name__ == "__main__":
    test_pnu_detail("2644010400103180045")
