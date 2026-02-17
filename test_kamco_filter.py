
import requests
import urllib.parse
import xml.etree.ElementTree as ET

KEYS = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

def test_kamco_filter(ctgr_id):
    url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
    key = KEYS[0]
    enc_key = urllib.parse.quote(key)
    
    query_params = [
        f"serviceKey={enc_key}",
        f"numOfRows=5",
        f"pageNo=1",
        f"DPSL_MTD_CD=0001",
        f"SIDO={urllib.parse.quote('경기도')}",
    ]
    if ctgr_id:
        query_params.append(f"CTGR_ID={ctgr_id}")
    
    full_url = f"{url}?{'&'.join(query_params)}"
    print(f"Testing URL: {full_url}")
    try:
        response = requests.get(full_url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response (first 500 chars): {response.text[:500]}")
            if '<response>' in response.text:
                root = ET.fromstring(response.text)
                body = root.find('body')
                header = root.find('header')
                if header is not None:
                    print(f"ResultCode: {header.find('resultCode').text}")
                if body is not None:
                    total_node = body.find('totalCount')
                    total = total_node.text if total_node is not None else 'N/A'
                    items = body.find('items')
                    print(f"Total Count: {total}")
                    if items is not None:
                        for item in items.findall('item'):
                            def get_t(node, tag):
                                el = node.find(tag)
                                return el.text if el is not None else ''
                            name = get_t(item, 'CLTR_NM')
                            goods = get_t(item, 'GOODS_NM')
                            print(f" - {name} ({goods})")
            else:
                print("No <response> tag found.")
    except Exception as e:
        print(f"Error: {e}")

print("--- Checking Land (10000) ---")
test_kamco_filter("10000")
print("\n--- Checking Building (20000) ---")
test_kamco_filter("20000")
print("\n--- Checking All (No CTGR_ID) ---")
test_kamco_filter(None)
