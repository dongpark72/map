import requests
import xml.etree.ElementTree as ET

PUBLIC_DATA_KEY = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"

def inspect_month(m):
    url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    params = {'serviceKey': PUBLIC_DATA_KEY, 'LAWD_CD': '26470', 'DEAL_YMD': m, 'numOfRows': 999}
    res = requests.get(url, params=params, timeout=10)
    if "<item>" in res.text:
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        for item in items:
            print(ET.tostring(item, encoding='unicode'))

if __name__ == "__main__":
    inspect_month("202202")
