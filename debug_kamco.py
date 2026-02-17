
import requests
import urllib.parse
import xml.etree.ElementTree as ET

# API Keys
KEYS = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"

def test_kamco(sido, sgk, key_idx=0):
    api_key = KEYS[key_idx]
    enc_key = urllib.parse.quote(api_key)
    
    params = {
        "serviceKey": enc_key,
        "pageNo": "1",
        "numOfRows": "500",
        "SIDO": sido,
        "SGK": sgk
    }
    
    # Manually construct query string to match exactly what standard libraries do, or just use requests params if trustworthy.
    # But here we double check encoding.
    
    # Just use requests param dict, typically safe enough. 
    # NOTE: data.go.kr keys often need double decoding or specific handling. 
    # Let's try sending decoded key in params (requests encodes it) first, if not try encoded.
    # The provided keys look Base64 encoded.
    
    try:
        # Request with decoded key (requests will URL-encode it)
        real_params = {
            "serviceKey": api_key, # requests will encode this
            "pageNo": 1,
            "numOfRows": 500,
            "SIDO": sido,
            "SGK": sgk
        }
        
        # NOTE: public data portal often requires the key to be passed unencoded in the URL string if it's already encoded, 
        # or encoded if it's not. It's messy. Let's try constructing the URL manually like in the proxy code.
        
        qs = f"?serviceKey={enc_key}&pageNo=1&numOfRows=500&SIDO={urllib.parse.quote(sido)}&SGK={urllib.parse.quote(sgk)}"
        full_url = url + qs
        
        print(f"Testing URL: {full_url}")
        response = requests.get(full_url, timeout=10)
        
        print(f"Status: {response.status_code}")
        # print(f"Response: {response.text[:500]}")
        
        if '<response>' in response.text:
            root = ET.fromstring(response.text)
            header = root.find('header')
            result_code = header.find('resultCode').text
            result_msg = header.find('resultMsg').text
            
            print(f"Result Code: {result_code}, Msg: {result_msg}")
            
            if result_code == '00':
                body = root.find('body')
                total = body.find('totalCount').text
                items = body.find('items')
                item_list = items.findall('item') if items else []
                print(f"Total Count: {total}, Retrieved: {len(item_list)}")
                
                # Search for target
                found = False
                for item in item_list:
                    addr = item.find('LDNM_ADRS').text or ""
                    road = item.find('NMRD_ADRS').text or ""
                    name = item.find('CLTR_NM').text or ""
                    
                    if '개포동' in addr and '14-1' in addr:
                        print(f"\n[FOUND!] {name} | {addr}")
                        found = True
                    elif '개포동' in addr:
                         # Print some nearby valid ones
                         # print(f" - Similar: {addr}")
                         pass
                
                if not found:
                    print("\nTarget '개포동 14-1' NOT found in this batch.")
            else:
                print("API Error.")
        else:
            print("Not XML response.")
            
    except Exception as e:
        print(f"Error: {e}")

print("--- Test 1: 서울특별시 강남구 ---")
test_kamco("서울특별시", "강남구")

print("\n--- Test 2: 서울 강남구 (Short Name) ---")
test_kamco("서울", "강남구")
