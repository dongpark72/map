
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def debug_full():
    url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    ek = urllib.parse.quote(key)
    
    pnu = "2644010400103180045"
    s = pnu[:5]; b = pnu[5:10]; pg = "0"; bun = "0318"; ji = "0045"
    
    apis = [
        ("Recap", "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"),
        ("Title", "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"),
        ("Basis", "http://apis.data.go.kr/1613000/BldRgstHubService/getBrBasisOulnInfo")
    ]
    
    for name, base in apis:
        q = f"{base}^serviceKey={ek}|numOfRows=10|sigunguCd={s}|bjdongCd={b}|platGbCd={pg}|bun={bun}|ji={ji}"
        r = requests.get(url, params={'url': q})
        print(f"\n--- {name} Results ---")
        if "<item>" in r.text:
            root = ET.fromstring(r.text)
            for it in root.findall('.//item'):
                pk = it.find('mgmBldrgstPk').text if it.find('mgmBldrgstPk') is not None else "N/A"
                bld = it.find('bldNm').text if it.find('bldNm') is not None else "N/A"
                area = it.find('totArea').text if it.find('totArea') is not None else "0"
                print(f"  PK:{pk} Name:{bld} Area:{area}")
                
                # Check floors for this PK
                qf = f"http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo^serviceKey={ek}|mgmBldrgstPk={pk}"
                rf = requests.get(url, params={'url': qf})
                fc = rf.text.count("<item>")
                print(f"    Floors: {fc}")
        else:
            print("  No items.")

if __name__ == "__main__":
    debug_full()
