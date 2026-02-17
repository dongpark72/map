import requests
import xml.etree.ElementTree as ET
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

def check_deal():
    keys = [os.getenv('PUBLIC_DATA_KEY_1'), os.getenv('PUBLIC_DATA_KEY_2')]
    sigungu_cd = "26530" # 부산 사상구
    deal_ymd = "202502"
    
    # Possible URLs
    urls = [
        "http://apis.data.go.kr/1613000/RTMSDataSvcIndTrade/getRTMSDataSvcIndTrade",
        "http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade"
    ]
    
    target_jibun = "507-20"
    target_price = "223000"
    
    found_any = False

    for url in urls:
        for key in keys:
            if not key: continue
            
            # Construct URL manually to avoid double encoding of the key
            # Public Data Portal keys often fail with requests' default param encoding
            # If the key contains '+', requests encodes it to '%2B'. 
            # But the portal sometimes expects either the raw '+' or the encoded '%2B' depending on the key type.
            # Usually, passing the already encoded key as is works best.
            
            full_url = f"{url}?serviceKey={key}&LAWD_CD={sigungu_cd}&DEAL_YMD={deal_ymd}"
            
            print(f"Checking URL: {url}")
            print(f"Key (start): {key[:10]}...")
            
            try:
                res = requests.get(full_url, timeout=10)
                if res.status_code == 200:
                    content = res.text
                    if "<item>" in content:
                        print("SUCCESS! Data found.")
                        root = ET.fromstring(content)
                        items = root.findall('.//item')
                        print(f"Total items: {len(items)}")
                        
                        for item in items:
                            def get_t(tag):
                                el = item.find(tag); return el.text.strip() if el is not None and el.text else ''
                            
                            price = get_t('거래금액').replace(',', '').strip()
                            umd = get_t('법정동').strip()
                            jibun = get_t('지번').strip()
                            
                            if (jibun == target_jibun or target_jibun in jibun) and price == target_price:
                                print("\n>>> MATCH FOUND! <<<")
                                print(f"Address: {umd} {jibun}")
                                print(f"Price: {price}만원")
                                print(f"Date: {get_t('년')}-{get_t('월')}-{get_t('일')}")
                                print(f"Area: {get_t('거래면적')} / {get_t('대지면적')}")
                                found_any = True
                                break
                        
                        if not found_any:
                            print("Target deal not in this response.")
                            # Show sample
                            for it in items[:3]:
                                print(f"  {get_t('법정동')} {get_t('지번')} - {get_t('거래금액')}")
                        else:
                            return # Exit if found
                    else:
                        print("No items in response.")
                        if "<resultCode>" in content:
                            print("Result Code:", content)
                else:
                    print(f"Fail: {res.status_code}")
            except Exception as e:
                print(f"Error: {e}")
            print("-" * 20)

if __name__ == "__main__":
    check_deal()
