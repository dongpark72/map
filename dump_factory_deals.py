import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()

def check_deal():
    key = os.getenv('PUBLIC_DATA_KEY_2')
    sigungu_cd = "26530" # 부산 사상구
    deal_ymd = "202502"
    url = "http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade"
    
    full_url = f"{url}?serviceKey={key}&LAWD_CD={sigungu_cd}&DEAL_YMD={deal_ymd}"
    
    print(f"Checking URL: {url} with Key 2")
    
    try:
        res = requests.get(full_url, timeout=10)
        if res.status_code == 200:
            content = res.text
            if "<item>" in content:
                root = ET.fromstring(content)
                items = root.findall('.//item')
                print(f"Total items found: {len(items)}")
                
                for i, item in enumerate(items):
                    print(f"\n--- Item {i+1} ---")
                    for child in item:
                        print(f"  {child.tag}: {child.text}")
                    
            else:
                print("No items in response.")
                print(content)
        else:
            print(f"Fail: {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_deal()
