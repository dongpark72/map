import requests
import urllib.parse
import os
import xml.etree.ElementTree as ET

# Only testing Key 2 as Key 1 fails 401
PUBLIC_DATA_KEY = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"

def check_address(sigungu, month, umd, jibun):
    url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    params = {'serviceKey': PUBLIC_DATA_KEY, 'LAWD_CD': sigungu, 'DEAL_YMD': month}
    
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            if "<item>" in res.text:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                print(f"Month {month}: Found {len(items)} total items in Sigungu.")
                for item in items:
                    def get_t(it, tag):
                        el = it.find(tag); return el.text.strip() if el is not None and el.text else ''
                    
                    item_umd = get_t(item, '법정동') or get_t(item, 'umdNm')
                    item_jibun = get_t(item, '지번') or get_t(item, 'jibun')
                    
                    if umd in item_umd and jibun in item_jibun:
                        print(f"  FOUND MATCH: {item_umd} {item_jibun}")
                        return True
            else:
                print(f"Month {month}: No items.")
        else:
            print(f"Month {month}: Status {res.status_code}")
    except Exception as e:
        print(f"Error {month}: {e}")
    return False

if __name__ == "__main__":
    # Check last 12 months for 감전동 147-3
    sigungu = "26470"
    umd = "감전동"
    jibun = "147-3"
    months = ["202511", "202510", "202509", "202508", "202507", "202506", "202505", "202411", "202311"]
    for m in months:
        if check_address(sigungu, m, umd, jibun):
            break
