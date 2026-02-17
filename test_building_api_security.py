
import os
import requests
import xml.etree.ElementTree as ET
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

pnu = "1111013700101000000"
sigunguCd = pnu[:5]
bjdongCd = pnu[5:10]
platGbCd = pnu[10]
bun = pnu[11:15]
ji = pnu[15:19]

PUBLIC_DATA_KEYS = [
    os.getenv('PUBLIC_DATA_KEY_1', ''),
    os.getenv('PUBLIC_DATA_KEY_2', ''),
]

print(f"Testing PNU: {pnu}")
print(f"Keys available: {bool(PUBLIC_DATA_KEYS[0])}, {bool(PUBLIC_DATA_KEYS[1])}")

api_url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

for key in PUBLIC_DATA_KEYS:
    if not key: continue
    enc_key = urllib.parse.quote(key)
    query = f"serviceKey={enc_key}&numOfRows=10&pageNo=1&sigunguCd={sigunguCd}&bjdongCd={bjdongCd}&platGbCd={platGbCd}&bun={bun}&ji={ji}"
    url = f"{api_url_title}?{query}"
    
    print(f"Calling API with key starting with {key[:10]}...")
    try:
        res = requests.get(url, timeout=10)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            if "<item>" in res.text:
                print("Success: Found items!")
                # print(res.text[:500])
            else:
                print("No items found or error in response.")
                print(res.text)
    except Exception as e:
        print(f"Error: {e}")
