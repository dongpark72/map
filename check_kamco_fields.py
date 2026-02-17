
import requests
import urllib.parse
import xml.etree.ElementTree as ET

KEYS = [
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

def test_kamco_all_fields():
    url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
    key = KEYS[0]
    
    query_params = [
        f"serviceKey={key}",
        f"numOfRows=1",
        f"pageNo=1",
        f"DPSL_MTD_CD=0001",
        f"CTGR_ID=10000",
        f"SIDO={urllib.parse.quote('경기도')}",
    ]
    
    full_url = f"{url}?{'&'.join(query_params)}"
    print(f"Testing URL: {full_url}")
    try:
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            body = root.find('body')
            if body is not None:
                items = body.find('items')
                if items is not None:
                    item = items.find('item')
                    if item is not None:
                        print("FIELDS FOUND IN LIST API:")
                        for child in item:
                            print(f"{child.tag}: {child.text}")
                    else:
                        print("No items found.")
                else:
                    print("No items node found.")
            else:
                print("No body found.")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

test_kamco_all_fields()
