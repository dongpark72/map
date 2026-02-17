import requests
import json

KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
BASIS_URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
HOSPITAL_NAME = "서울대학교어린이병원"

def debug_basis_structure():
    print(f"Searching for: {HOSPITAL_NAME}")
    params = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '1',
        '_type': 'json',
        'yadmNm': HOSPITAL_NAME
    }
    
    try:
        res = requests.get(BASIS_URL, params=params, timeout=10)
        print(f"Status: {res.status_code}")
        
        data = res.json()
        print(f"Data type: {type(data)}")
        # print(json.dumps(data, indent=2, ensure_ascii=False))
        
        resp = data.get('response')
        print(f"'response' type: {type(resp)}")
        if not isinstance(resp, dict):
            print(f"'response' content: {resp}")
            return

        body = resp.get('body')
        print(f"'body' type: {type(body)}")
        if not isinstance(body, dict):
             print(f"'body' content: {body}")
             return

        items_container = body.get('items')
        print(f"'items' container type: {type(items_container)}")
        if not isinstance(items_container, dict):
             print(f"'items' container content: {items_container}")
             return

        item = items_container.get('item')
        print(f"'item' type: {type(item)}")
        print(f"'item' content: {item}")
        
        if isinstance(item, list):
            print("Item is a list.")
            print(f"First element type: {type(item[0])}")
            item[0].get('ykiho')
        else:
            print("Item is NOT a list.")
            try:
                item.get('ykiho')
                print("item.get('ykiho') succeeded.")
            except AttributeError:
                print("item.get('ykiho') FAILED: 'str' object has no attribute 'get'")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    debug_basis_structure()
