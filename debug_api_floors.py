
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def test_pnu_api(pnu):
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    service_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    enc_key = urllib.parse.quote(service_key)
    
    sigungu = pnu[:5]
    bjdong = pnu[5:10]
    platGb = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15])).zfill(4)
    ji = str(int(pnu[15:19])).zfill(4)
    
    apis = [
        "getBrRecapTitleInfo",
        "getBrTitleInfo",
        "getBrBasisOulnInfo"
    ]
    
    site_pks = []
    print(f"--- Querying PNU: {pnu} ---")
    
    for api in apis:
        url = f"http://apis.data.go.kr/1613000/BldRgstHubService/{api}"
        q = f"{url}^serviceKey={enc_key}|numOfRows=10|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
        try:
            res = requests.get(connector_url, params={'url': q}, timeout=10)
            if res.status_code == 200:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                print(f"API {api}: found {len(items)} items")
                for it in items:
                    pk = it.find('mgmBldrgstPk').text if it.find('mgmBldrgstPk') is not None else "N/A"
                    bld_nm = it.find('bldNm').text if it.find('bldNm') is not None else "N/A"
                    print(f"  - PK: {pk}, Name: {bld_nm}")
                    if pk != "N/A":
                        site_pks.append(pk)
        except Exception as e:
            print(f"API {api} failed: {e}")
            
    if site_pks:
        main_pk = site_pks[0]
        print(f"\n--- Querying Floors for PK: {main_pk} ---")
        url_flr = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
        q_f = f"{url_flr}^serviceKey={enc_key}|numOfRows=100|mgmBldrgstPk={main_pk}"
        try:
            res_f = requests.get(connector_url, params={'url': q_f}, timeout=10)
            if res_f.status_code == 200:
                root_f = ET.fromstring(res_f.text)
                items_f = root_f.findall('.//item')
                print(f"Floors: found {len(items_f)} items")
                for f in items_f[:5]: # print first 5
                    flr = f.find('flrNoNm').text if f.find('flrNoNm') is not None else "N/A"
                    purp = f.find('mainPurpsCdNm').text if f.find('mainPurpsCdNm') is not None else "N/A"
                    area = f.find('area').text if f.find('area') is not None else "N/A"
                    print(f"  - Floor: {flr}, Purpose: {purp}, Area: {area}")
        except Exception as e:
            print(f"Floor API failed: {e}")

if __name__ == "__main__":
    # 부산 영도구 동삼동 318-45
    test_pnu_api("2644010400103180045")
