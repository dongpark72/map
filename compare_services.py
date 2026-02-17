
import requests
import sys
import urllib.parse
import xml.dom.minidom

# Configuration
# Service 1: Unified Usage (from latest screenshot)
URL_UNIFY = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"

# Service 2: Kamco Public Sale (from earlier screenshot, likely source of desired fields)
URL_KAMCO = "http://openapi.onbid.co.kr/openapi/services/KamcoPblsalThingInquireSvc/getKamcoPbctCltrList"

KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

def print_response(title, response):
    print(f"\n--- {title} ---")
    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")
    try:
        if response.text.strip().startswith('<'):
             dom = xml.dom.minidom.parseString(response.text)
             print(dom.toprettyxml(indent="  ")[:1000]) # First 1000 chars
        else:
             print(response.text[:500])
    except:
        print(response.text[:500])

def test_unify():
    # Testing 'getUnifyUsageCltr'
    # Valid params for this usually are: serviceKey, pageNo, numOfRows, sido, sgk, etc.
    # Note: Params are usually lower case or camelCase in standard GoDatagokr, 
    # but Onbid might use UPPERCASE as per their specific doc.
    # Let's try both casing if one fails? Or stick to the screenshot (Screenshot 3 shows SIDO, SGK)
    
    # Mimic Chrome on Windows 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }

    try:
        r = requests.get(URL_UNIFY, params=params, headers=headers, timeout=10)
        print_response("Testing getUnifyUsageCltr (Unified Info)", r)
    except Exception as e:
        print(f"Unify Test Failed: {e}")

def test_kamco():
    # Testing 'getKamcoPbctCltrList'
    # Requires DPSL_MTD_CD
    params = {
        'serviceKey': KEY,
        'numOfRows': '10',
        'pageNo': '1',
        'DPSL_MTD_CD': '0001', # Sale
        'SIDO': '서울특별시',
        'SGK': '강남구'
    }
    
    # Mimic Chrome on Windows 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }

    try:
        r = requests.get(URL_KAMCO, params=params, headers=headers, timeout=10)
        print_response("Testing getKamcoPbctCltrList (Kamco Auction)", r)

    except Exception as e:
        print(f"Kamco Test Failed: {e}")

if __name__ == "__main__":
    test_unify()
    test_kamco()
