
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def test_building_proxy_v2():
    pnu = "1111013800101550002"
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    base_urls = {
        'Recap': "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo",
        'Title': "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo",
        'Expos': "http://apis.data.go.kr/1613000/BldRgstHubService/getBrExposPubuseAreaInfo", # Jeonyu? No, Jeonyubu is getBrExposInfo? 
        # Actually standard Jeonyubu is getBrExposPubuseAreaInfo? Or getBrExposInfo?
        # Let's try getBrTitleInfo first.
        'Basis': "http://apis.data.go.kr/1613000/BldRgstHubService/getBrBasisOulnInfo"
    }

    # API Keys
    keys = [
        "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
        "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
    ]
    
    # Parse PNU
    sigungu = pnu[0:5]
    bjdong = pnu[5:10]
    # Try both platGb definitions
    # Standard: 1 -> 0 (General), 2 -> 1 (San)
    # But usually PNU 11th char is 1 (General) or 2 (San).
    # API expects '0' for General, '1' for San.
    # If PNU char is '1', we send '0'.
    
    bun = str(int(pnu[11:15])).zfill(4)
    ji = str(int(pnu[15:19])).zfill(4)
    
    variations = [
        {'platGbCd': '0', 'desc': 'General (0)'},
        {'platGbCd': '1', 'desc': 'San (1)'}
    ]

    for var in variations:
        print(f"--- Testing Variant: {var['desc']} ---")
        platGb = var['platGbCd']
        
        for name, url in base_urls.items():
            print(f"  Querying {name}...")
            # Try keys
            for key in keys:
                enc_key = urllib.parse.quote(key)
                q = f"{url}^serviceKey={enc_key}|numOfRows=10|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
                try:
                    res = session.get(connector_url, params={'url': q}, timeout=5)
                    if res.status_code == 200:
                        if '<errMsg>' in res.text:
                            # print(f"    Error Msg: {res.text[:100]}")
                            pass
                        elif '<items>' in res.text:
                            items = ET.fromstring(res.text).findall('.//item')
                            print(f"    SUCCESS: Found {len(items)} items")
                            if items:
                                print(f"    Sample: {items[0].find('bldNm').text if items[0].find('bldNm') is not None else 'NoName'}")
                                break # Stop keys loop if found
                    else:
                        print(f"    Status {res.status_code}")
                except Exception as e:
                    print(f"    Exception: {e}")

if __name__ == "__main__":
    test_building_proxy_v2()
