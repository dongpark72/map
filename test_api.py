import requests
import urllib.parse
import xml.etree.ElementTree as ET

api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
sigungu_cd = "26440" # Busan Sasang-gu

months = ["202410", "202409", "202408", "202312", "202311"]
api_url = "http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade"

for month in months:
    enc_key = urllib.parse.quote(api_key)
    query = f"serviceKey={enc_key}&LAWD_CD={sigungu_cd}&DEAL_YMD={month}"
    url = f"{api_url}?{query}"
    
    print(f"--- Month: {month} ---")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if "<item>" in response.text:
            root = ET.fromstring(response.text)
            items = root.findall('.//item')
            print(f"Found {len(items)} items.")
            for item in items[:2]:
                addr = item.find('umdNm').text if item.find('umdNm') is not None else '?'
                jibun = item.find('jibun').text if item.find('jibun') is not None else '?'
                price = item.find('dealAmount').text if item.find('dealAmount') is not None else '?'
                print(f"  {addr} {jibun}: {price}")
        else:
            if "<items/>" in response.text or "<items />" in response.text:
                print("  No items found.")
            else:
                print("  Unexpected response:")
                print(response.text[:200])
    except Exception as e:
        print(f"Error: {e}")
