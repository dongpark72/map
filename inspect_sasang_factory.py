import requests
import xml.etree.ElementTree as ET
import urllib.parse
import sys

# Configuration
API_KEY_DEC = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
API_KEY_ENC = urllib.parse.quote(API_KEY_DEC)
LAWD_CD = "26530" # Busan Sasang-gu
Target_Dong = "감전동"

# Factory/Industrial Trade API URL
API_URL = "http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade"
# Use Connector URL to bypass local restrictions (simulating backend)
URL = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"

def check_month(month):
    print(f"\n--- Checking {month} ---")
    # Format query for the connector
    query = f"{API_URL}^serviceKey={API_KEY_ENC}|LAWD_CD={LAWD_CD}|DEAL_YMD={month}"
    
    try:
        # Pass the full query as 'url' parameter to the connector
        response = requests.get(URL, params={'url': query}, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            print(f"Error: Status Code {response.status_code}")
            return

        try:
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
        except ET.ParseError:
            print(f"XML Parse Error. Raw response (decoded):", response.content.decode('utf-8', errors='replace')[:500])
            return
            
        if not items:
            print("No data found for this month.")
            return

        print(f"Total Items: {len(items)}")
        
        found_target = False
        for item in items:
            def get_val(tag):
                node = item.find(tag)
                return node.text.strip() if node is not None and node.text else ""

            dong = get_val("법정동") or get_val("umdNm")
            jibun = get_val("지번") or get_val("jibun")
            b_type = get_val("건물유형") or get_val("buildingType")
            price = get_val("거래금액") or get_val("dealAmount")
            day = get_val("일") or get_val("dealDay")
            
            # Print ALL items briefly
            # print(f"[{dong}] {jibun} ({b_type}) - {price}")

            if Target_Dong in dong:
                found_target = True
                print(f"  >>> MATCH FOUND: [{dong}] {jibun} | {b_type} | {price} | Day: {day}")

        if not found_target:
            print(f"  (No matches for {Target_Dong} in this month)")

    except Exception as e:
        print(f"Exception: {e}")

# Check last 12 months
months_to_check = [
    "202502", "202501", 
    "202412", "202411", "202410", "202409", 
    "202408", "202407", "202406", "202405", "202404", "202403"
]

print(f"Checking Factory Trades for {Target_Dong} (Sasang-gu {LAWD_CD})")
for m in months_to_check:
    check_month(m)
