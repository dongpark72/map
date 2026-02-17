
import requests
import urllib.parse
import xml.etree.ElementTree as ET

# Building API (known to work with Key 1)
URL = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
KEY1 = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
KEY2_HEX = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def check_key(name, k, is_hex=False):
    print(f"\n--- Checking {name} on Building API ---")
    try:
        # Standard PNU (Guri-si Sutaek-dong) - just a random valid one or generic
        # Using SigunguCd and BjdongCd for Guri (41310, 10500)
        params = {
            'sigunguCd': '41310',
            'bjdongCd': '10500', 
            'numOfRows': '1', 
            'pageNo': '1'
        }
        
        # Encoding logic
        if is_hex:
            service_key = k # No encoding needed? Or maybe it needs to be unquoted?
            # actually requests encodes everything in params. 
            # If we want to send it raw, we must use string.
        else:
            service_key = urllib.parse.unquote(k) # requests will quote it back. 
            # Wait, usually we pass the Decoded key to requests.
            # KEY1 provided is Base64. It might be the "Encoding" key (already encoded) or "Decoding" key.
            # Usually we use the "Decoding" key with requests.
        
        # Let's just try sending it manually constructed to be sure
        
        enc_k = k if is_hex else urllib.parse.quote(k) # If base64, quote it.
        
        qs = f"?serviceKey={enc_k}&sigunguCd=41310&bjdongCd=10500&platGbCd=0&bun=0000&ji=0000&numOfRows=1&pageNo=1"
        r = requests.get(URL + qs, headers=headers, timeout=5)
        
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text[:200]}")
        
        if '<resultCode>00' in r.text or '<item>' in r.text:
            print("SUCCESS: Valid Key for Building API")
        else:
            print("FAILED: Invalid Key for Building API")
            
    except Exception as e:
        print(e)
        
check_key("Key 1 (Base64)", KEY1, False)
check_key("Key 2 (Hex)", KEY2_HEX, True)
