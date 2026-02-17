import requests
import xml.etree.ElementTree as ET

pnu = "2644010400107900000" 

def test_fetch():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
    }
    session.headers.update(headers)

    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    api_url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

    keys_to_try = [
        "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
        "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368",
    ]
    
    pnus_to_try = [pnu]
    if pnu.startswith('2644010400'):
        alt_pnu = '2644010100' + pnu[10:]
        pnus_to_try.append(alt_pnu)
        print(f"Added alternative PNU: {alt_pnu}")

    for target_pnu in pnus_to_try:
        sigungu = target_pnu[0:5]
        bjdong = target_pnu[5:10]
        platGb = '0' if target_pnu[10] == '1' else '1'
        bun = str(int(target_pnu[11:15])).zfill(4) 
        ji = str(int(target_pnu[15:19])).zfill(4)

        print(f"\nTesting PNU: {target_pnu}")

        for api_key in keys_to_try:
            print(f"  Trying Key: {api_key[:10]}...")
            q_title = f"{api_url_title}^serviceKey={api_key}|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}|numOfRows=999"
            
            try:
                res_title = session.get(connector_url, params={'url': q_title}, timeout=10)
                
                if res_title.status_code == 200:
                    try:
                        root = ET.fromstring(res_title.text)
                        
                        total_cnt_node = root.find('.//totalCount')
                        total_cnt = total_cnt_node.text if total_cnt_node is not None else "Unknown"
                        
                        items = root.findall('.//item')
                        print(f"    Total Count: {total_cnt}, Items: {len(items)}")

                        for i, item in enumerate(items):
                            bldNm = item.find('bldNm').text if item.find('bldNm') is not None else ''
                            dongNm = item.find('dongNm').text if item.find('dongNm') is not None else ''
                            print(f"      [{i+1}] {bldNm} (Dong: {dongNm})")
                        
                        if items:
                            return # Stop if found
                    except Exception as e:
                        print(f"    XML Parse Error: {e}")
            except Exception as e:
                print(f"    Request Error: {e}")

if __name__ == "__main__":
    test_fetch()
