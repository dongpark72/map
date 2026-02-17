
import requests
import urllib.parse
import xml.etree.ElementTree as ET

url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
key_dec = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def test_encoding(enc_name):
    print(f"\nTesting {enc_name}...")
    try:
        sido_enc = urllib.parse.quote('서울특별시'.encode(enc_name))
        sgk_enc = urllib.parse.quote('강남구'.encode(enc_name))
        key_enc = urllib.parse.quote(key_dec)
        
        qs = f"?serviceKey={key_enc}&pageNo=1&numOfRows=10&SIDO={sido_enc}&SGK={sgk_enc}"
        r = requests.get(url + qs, headers=headers, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text[:200]}")
    except Exception as e:
        print(e)
        
test_encoding('utf-8')
test_encoding('euc-kr')
