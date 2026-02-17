
import requests
import xml.etree.ElementTree as ET
import urllib.parse
import json

def debug_pnus():
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    enc_key = urllib.parse.quote(key)
    
    # Target: 부산 영도구 동삼동 318-45
    pnus = ["2644010400103180045", "2644010100103180045"]
    apis = [
        "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo",
        "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo",
        "http://apis.data.go.kr/1613000/BldRgstHubService/getBrBasisOulnInfo"
    ]
    
    for p in pnus:
        sigungu = p[:5]
        bjdong = p[5:10]
        platGb = '0' if p[10] == '1' else '1'
        bun = str(int(p[11:15])).zfill(4)
        ji = str(int(p[15:19])).zfill(4)
        print(f"\n>>>> Testing PNU: {p} (platGbCd={platGb}, bun={bun}, ji={ji}) <<<<")
        
        for api_url in apis:
            api_name = api_url.split('/')[-1]
            q = f"{api_url}^serviceKey={enc_key}|numOfRows=10|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
            try:
                res = requests.get(connector_url, params={'url': q}, timeout=10)
                if "<item>" in res.text:
                    root = ET.fromstring(res.text)
                    items = root.findall('.//item')
                    print(f"[{api_name}] Found {len(items)} items")
                    for it in items:
                        pk = it.find('mgmBldrgstPk').text if it.find('mgmBldrgstPk') is not None else "N/A"
                        bld_nm = it.find('bldNm').text if it.find('bldNm') is not None else "N/A"
                        tot_area = it.find('totArea').text if it.find('totArea') is not None else "0"
                        print(f"  - PK: {pk}, Name: {bld_nm}, TotArea: {tot_area}")
                        
                        # Try floors
                        url_flr = f"http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo^serviceKey={enc_key}|numOfRows=100|mgmBldrgstPk={pk}"
                        res_f = requests.get(connector_url, params={'url': url_flr}, timeout=5)
                        f_count = res_f.text.count("<item>")
                        print(f"    -> Floor info results: {f_count} items")
                else:
                    print(f"[{api_name}] No items found.")
            except Exception as e:
                print(f"[{api_name}] Error: {e}")

if __name__ == "__main__":
    debug_pnus()
