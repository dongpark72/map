import requests
import xml.etree.ElementTree as ET

PUBLIC_DATA_KEY = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"

def test_month(m):
    url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    params = {'serviceKey': PUBLIC_DATA_KEY, 'LAWD_CD': '26470', 'DEAL_YMD': m, 'numOfRows': 999}
    try:
        res = requests.get(url, params=params, timeout=10)
        if "<item>" in res.text:
            root = ET.fromstring(res.text)
            items = root.findall('.//item')
            return len(items)
    except: pass
    return 0

if __name__ == "__main__":
    for y in [2024, 2023, 2022]:
        for m in range(12, 0, -1):
            ym = f"{y}{m:02d}"
            cnt = test_month(ym)
            if cnt > 0:
                print(f"{ym}: Found {cnt} items")
            else:
                print(f"{ym}: 0")
