
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def deep_search():
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    keys = [
        "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
        "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
    ]
    
    # 부산 영도구 동삼동 318-45
    sigunguCd = "26440"
    bjdongCd = "10400"
    bun = "0318"
    ji = "0045"
    
    apis = ["getBrTitleInfo", "getBrRecapTitleInfo", "getBrBasisOulnInfo"]
    
    for key in keys:
        ek = urllib.parse.quote(key)
        for api in apis:
            for plat in ["0", "1"]:
                url = f"http://apis.data.go.kr/1613000/BldRgstHubService/{api}"
                q = f"{url}^serviceKey={ek}|numOfRows=10|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={plat}|bun={bun}|ji={ji}"
                try:
                    res = requests.get(connector_url, params={'url': q}, timeout=10)
                    if "<item>" in res.text:
                        print(f"SUCCESS: {api} with plat={plat} and key={key[:10]}...")
                        # print(res.text[:500])
                        return
                    else:
                        print(f"FAIL: {api} plat={plat} key={key[:10]}...")
                except:
                    print(f"ERROR: {api}")

if __name__ == "__main__":
    deep_search()
