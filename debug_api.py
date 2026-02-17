import requests
import xml.etree.ElementTree as ET

# Configuration
pnu = "2644010100107900000"
sigungu = pnu[0:5]
bjdong = pnu[5:10]
platGb = '0' if pnu[10] == '1' else '1'
bun = str(int(pnu[11:15])).zfill(4)
ji = str(int(pnu[15:19])).zfill(4)

keys = [
    "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
    "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
]

apis = {
    "Recap (Total)": "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo",
    "Title (General)": "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo",
    "Floor (Detail)": "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
}

print(f"--- Diagnosing PNU: {pnu} ---")
print(f"Params: sigungu={sigungu}, bjdong={bjdong}, platGb={platGb}, bun={bun}, ji={ji}")

for k_idx, key in enumerate(keys):
    print(f"\n[Key #{k_idx+1}]: {key[:10]}...")
    
    for name, url in apis.items():
        try:
            params = {
                'serviceKey': requests.utils.unquote(key), # Try unquoted first
                'sigunguCd': sigungu,
                'bjdongCd': bjdong,
                'platGbCd': platGb,
                'bun': bun,
                'ji': ji,
                'numOfRows': 200
            }
            # Note: ServiceKey handling in requests is tricky, better to construct query string manually or use unquote
            # Python requests encodes parameters automatically. If key is already encoded, we might double encode.
            # Usually public data portal keys need to be passed AS IS (decoded) to requests so it encodes them,
            # OR passed as string in url.
            
            # Let's try manual construction to be safe like the browser/server
            query = f"?serviceKey={key}&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}&numOfRows=200"
            full_url = url + query
            
            res = requests.get(full_url, timeout=5)
            
            if res.status_code == 200:
                root = ET.fromstring(res.text)
                header_code = root.find('.//resultCode')
                code = header_code.text if header_code is not None else 'Unknown'
                
                items = root.findall('.//item')
                print(f"  > {name}: Status {code}, Items Found: {len(items)}")
                
                if items:
                    for i, item in enumerate(items[:3]): # Show first 3
                        bldNm = item.find('bldNm').text if item.find('bldNm') is not None else ''
                        dongNm = item.find('dongNm').text if item.find('dongNm') is not None else ''
                        print(f"    - Item {i+1}: {bldNm} {dongNm}")
                    
                    # Specifically check for dong names in Floor API
                    if name == "Floor (Detail)":
                        dongs = set()
                        for item in items:
                            d = item.find('dongNm')
                            if d is not None and d.text:
                                dongs.add(d.text)
                        print(f"    -> Unique Dongs in Floor Info: {dongs}")
            else:
                print(f"  > {name}: HTTP {res.status_code}")
                
        except Exception as e:
            print(f"  > {name}: Error {e}")
