import requests
import xml.etree.ElementTree as ET
import os
import urllib.parse

# Decoded key might be needed for direct call if using params
PUBLIC_DATA_KEY_RAW = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="

def check_factory_direct(sigungu, month):
    urls = [
        'http://apis.data.go.kr/1613000/RTMSDataSvcIndTrade/getRTMSDataSvcIndTrade',
        'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    ]
    
    for url in urls:
        params = {
            'serviceKey': PUBLIC_DATA_KEY_RAW,
            'LAWD_CD': sigungu,
            'DEAL_YMD': month
        }
        try:
            res = requests.get(url, params=params, timeout=10)
            print(f"URL: {url}")
            print(f"Status: {res.status_code}")
            print(f"Response (300 chars): {res.text[:300]}")
            if "<item>" in res.text:
                print("SUCCESS!")
                return True
        except Exception as e:
            print(f"Error: {e}")
    return False

if __name__ == "__main__":
    check_factory_direct("26470", "202411")
