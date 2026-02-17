
import requests
import urllib.parse
import xml.etree.ElementTree as ET

url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
key_dec = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

print("1. Testing with requests params (Standard encoding)...")
try:
    params = {
        'serviceKey': key_dec,
        'pageNo': '1',
        'numOfRows': '10',
        'SIDO': '서울특별시',
        'SGK': '강남구'
    }
    r = requests.get(url, params=params, headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Values: {r.text[:200]}")
except Exception as e:
    print(e)
    
print("\n2. Testing with manual query string (Pre-encoded)...")
try:
    key_enc = urllib.parse.quote(key_dec)
    qs = f"?serviceKey={key_enc}&pageNo=1&numOfRows=10&SIDO={urllib.parse.quote('서울특별시')}&SGK={urllib.parse.quote('강남구')}"
    r = requests.get(url + qs, headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Values: {r.text[:200]}")
except Exception as e:
    print(e)
