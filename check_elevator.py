
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def check_elevator(pnu):
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    service_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    enc_key = urllib.parse.quote(service_key)
    
    sigungu = pnu[:5]
    bjdong = pnu[5:10]
    platGb = '0' if pnu[10] == '1' else '1'
    bun = str(int(pnu[11:15])).zfill(4)
    ji = str(int(pnu[15:19])).zfill(4)
    
    print(f"Checking PNU: {pnu}")
    print(f"Params: sigungu={sigungu}, bjdong={bjdong}, platGb={platGb}, bun={bun}, ji={ji}")

    apis = [
        ("getBrRecapTitleInfo", "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"),
        ("getBrTitleInfo", "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo")
    ]
    
    for api_name, api_url in apis:
        print(f"\n--- API: {api_name} ---")
        q = f"{api_url}^serviceKey={enc_key}|numOfRows=10|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
        
        try:
            res = requests.get(connector_url, params={'url': q}, timeout=10)
            if res.status_code == 200:
                if '<response>' in res.text:
                    root = ET.fromstring(res.text)
                    items = root.findall('.//item')
                    print(f"Items found: {len(items)}")
                    
                    if items:
                        item = items[0]
                        print("First Item Fields:")
                        for child in item:
                            if 'elvt' in child.tag.lower() or 'elevator' in child.tag.lower() or 'lift' in child.tag.lower():
                                print(f"  [FOUND ELEVATOR FIELD] {child.tag}: {child.text}")
                            else:
                                # Uncomment to see all fields
                                print(f"  {child.tag}: {child.text}")
                else:
                    print("Response valid but no XML/Items found (or error in response text).")
            else:
                print(f"Status Code: {res.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Test with Gangnam Kyobo Tower
    check_elevator("1165010800113030022")
    
