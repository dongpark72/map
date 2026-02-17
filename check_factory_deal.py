import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()

def check_deal():
    # Use raw key. Requests will encode it if we pass it in params.
    # But wait, sometimes the key itself contains '+' or '/' which are already encoded or need to be.
    # The key in .env looks like a Base64 encoded string, which is common for Public Data Portal.
    api_key = os.getenv('PUBLIC_DATA_KEY_1')
    if not api_key:
        print("API Key not found in .env")
        return

    # parameters
    sigungu_cd = "26530" # 부산 사상구
    deal_ymd = "202502"
    
    # Try direct URL
    api_url = "http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade"
    
    params = {
        'serviceKey': api_key,
        'LAWD_CD': sigungu_cd,
        'DEAL_YMD': deal_ymd
    }
    
    print(f"Calling API directly for {sigungu_cd} {deal_ymd}...")
    
    try:
        # Note: sometimes we need to pass the key as is (unquoted) in the URL string
        # because requests might double-encode it.
        # Let's try regular params first.
        res = requests.get(api_url, params=params, timeout=15)
        print(f"Status Code: {res.status_code}")
        
        if res.status_code == 200:
            content = res.text
            print("Response length:", len(content))
            if len(content) < 500:
                print("Response Content:", content)
            
            if "<item>" in content:
                root = ET.fromstring(content)
                items = root.findall('.//item')
                print(f"Found {len(items)} items.")
                
                target_jibun = "507-20"
                target_price = "223000" # 223,000만원
                
                found = False
                for item in items:
                    def get_t(tag):
                        el = item.find(tag); return el.text.strip() if el is not None and el.text else ''
                    
                    price = get_t('거래금액').replace(',', '').strip()
                    umd = get_t('법정동').strip()
                    jibun = get_t('지번').strip()
                    
                    # print(f"Deal: {umd} {jibun} - {price}만원")
                    
                    if (jibun == target_jibun or target_jibun in jibun) and price == target_price:
                        print("\n>>> MATCH FOUND! <<<")
                        print(f"Address: {umd} {jibun}")
                        print(f"Price: {price}만원")
                        print(f"Date: {get_t('년')}-{get_t('월')}-{get_t('일')}")
                        print(f"Area: {get_t('거래면어')} / {get_t('대지면적')}")
                        found = True
                
                if not found:
                    print("\nTarget deal NOT found in this month's data.")
                    # Show first few items to see what's there
                    for i, item in enumerate(items[:5]):
                        def get_t(tag):
                            el = item.find(tag); return el.text.strip() if el is not None and el.text else ''
                        print(f"Sample {i+1}: {get_t('법정동')} {get_t('지번')} - {get_t('거래금액')}만원")
            else:
                if "SERVICE_KEY_IS_NOT_REGISTERED_ERROR" in content:
                    print("Error: Service Key is not registered.")
                elif "LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR" in content:
                    print("Error: Request limit exceeded.")
                else:
                    print("No items found or different format.")
        else:
            print(f"Request failed with status {res.status_code}")
            print(res.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_deal()
