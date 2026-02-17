import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()

# From views.py
PUBLIC_DATA_KEYS = [
    os.getenv('PUBLIC_DATA_KEY_1', ''),
    os.getenv('PUBLIC_DATA_KEY_2', ''),
]
CONNECTOR_URL = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"

def test_real_price(pnu, p_type, month):
    sigungu_cd = pnu[:5]
    api_map = {
        'apt': 'http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev',
        'land': 'http://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade',
        'offi': 'http://apis.data.go.kr/1613000/RTMSDataSvcOffiTrade/getRTMSDataSvcOffiTrade',
        'row': 'http://apis.data.go.kr/1613000/RTMSDataSvcRHTrade/getRTMSDataSvcRHTrade',
        'detached': 'http://apis.data.go.kr/1613000/RTMSDataSvcSHTrade/getRTMSDataSvcSHTrade',
        'biz': 'http://apis.data.go.kr/1613000/RTMSDataSvcNrgTrade/getRTMSDataSvcNrgTrade',
        'factory': 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    }
    api_url = api_map.get(p_type)
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    for api_key in PUBLIC_DATA_KEYS:
        if not api_key: continue
        import urllib.parse
        enc_key = urllib.parse.quote(api_key)
        query = f"{api_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={month}"
        
        print(f"Testing {p_type} for {month} with key {api_key[:10]}...")
        try:
            res = session.get(CONNECTOR_URL, params={'url': query}, timeout=10)
            print(f"Status: {res.status_code}")
            print(f"Encoding (requests detected): {res.encoding}")
            print(f"Apparent Encoding: {res.apparent_encoding}")
            
            # Print a bit of the raw content to see if it's garbled
            print("Raw content snippet (hex):", res.content[:50].hex())
            
            # Print text snippet
            try:
                print("Text snippet (default):", res.text[:200])
            except Exception as e:
                print("Text snippet error:", e)
                
            # Try decoding with apparent encoding
            try:
                text_corrected = res.content.decode(res.apparent_encoding or 'utf-8')
                print("Text snippet (corrected):", text_corrected[:200])
                
                if "<item>" in text_corrected:
                    root = ET.fromstring(text_corrected)
                    items = root.findall('.//item')
                    if items:
                        print(f"Found {len(items)} items!")
                        for i, item in enumerate(items[:2]):
                            for child in item:
                                print(f"  {child.tag}: {child.text}")
            except Exception as e:
                print("Correction error:", e)
                
        except Exception as e:
            print(f"Request error: {e}")

if __name__ == "__main__":
    pnu = "1174010500100560000" # 서울 강동구 명일동 56
    test_real_price(pnu, "apt", "202412")
    test_real_price(pnu, "land", "202412")
