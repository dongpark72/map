import requests
import xml.etree.ElementTree as ET

PUBLIC_DATA_KEY = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"

def test_service(url, name):
    params = {'serviceKey': PUBLIC_DATA_KEY, 'LAWD_CD': '26470', 'DEAL_YMD': '202511'}
    try:
        res = requests.get(url, params=params, timeout=10)
        print(f"Service {name}: Status {res.status_code}")
        if "<item>" in res.text:
            root = ET.fromstring(res.text)
            print(f"  SUCCESS! Found {len(root.findall('.//item'))} items.")
        else:
            print(f"  No items. Snippet: {res.text[:200].strip()}")
    except Exception as e:
        print(f"  Error {name}: {e}")

if __name__ == "__main__":
    test_service('http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade', 'InduTrade')
    test_service('http://apis.data.go.kr/1613000/RTMSDataSvcIndTrade/getRTMSDataSvcIndTrade', 'IndTrade')
    test_service('http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev', 'AptTrade')
