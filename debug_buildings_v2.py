import requests
import xml.etree.ElementTree as ET

pnu = "2642010200103690009" # 부산광역시 사상구 덕포동 369-9
sigunguCd = pnu[0:5]
bjdongCd = pnu[5:10]
# Try both platGbCd 0 and 1
for platGb in ['0', '1']:
    bun = str(int(pnu[11:15])) # Remove leading zeros
    ji = str(int(pnu[15:19]))
    
    print(f"Testing platGbCd={platGb}, bun={bun}, ji={ji}")

    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    api_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
    api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    q = f"{api_url}^serviceKey={api_key}|sigunguCd={sigunguCd}|bjdongCd={bjdongCd}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=100"

    try:
        res = requests.get(connector_url, params={'url': q}, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.text)
            items = root.findall('.//item')
            print(f" -> Found {len(items)} buildings.")
            for item in items:
                bldNm = item.find('bldNm').text if item.find('bldNm') is not None else ''
                dongNm = item.find('dongNm').text if item.find('dongNm') is not None else ''
                print(f"    Building: {bldNm}, Dong: {dongNm}")
    except Exception as e:
        print(f" -> Error: {e}")
