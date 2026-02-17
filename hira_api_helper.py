import requests
import urllib.parse
import json

# 이 키는 사용자의 .env에 있는 'PUBLIC_DATA_KEY_1' 입니다.
# 만약 키 문제가 해결되면 이 코드는 즉시 작동할 것입니다.
API_KEY = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
BASIS_URL = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"

def get_ykiho(hospital_name):
    """
    병원명으로 ykiho(암호화된 요양기호)를 조회합니다.
    """
    print(f"Searching ykiho for: {hospital_name}")
    
    encoded_key = urllib.parse.quote(API_KEY)
    
    # 파라미터 구성
    params = {
        'pageNo': '1',
        'numOfRows': '10', # 이름이 비슷할 수 있으니 10개 정도 가져옴
        '_type': 'json',
        # 'yadmNm': hospital_name # requests가 인코딩해줌
    }
    
    # URL에 ServiceKey 직접 붙이기 (이중 인코딩 방지)
    url_with_key = f"{BASIS_URL}?ServiceKey={encoded_key}"
    
    try:
        # yadmNm 등 나머지 파라미터는 requests params로 전달
        # 주의: yadmNm은 params에 넣으면 requests가 자동으로 URL Encoding 함.
        res = requests.get(url_with_key, params={'yadmNm': hospital_name, **params}, timeout=10)
        
        print(f"Status: {res.status_code}")
        
        if res.status_code != 200:
            print(f"Error Response: {res.text[:200]}")
            return None
            
        data = None
        try:
            data = res.json()
        except:
            print("Failed to parse JSON. Response might be XML or Error HTML.")
            print(res.text[:200])
            return None
            
        # 데이터 파싱
        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
        
        if isinstance(items, dict):
            items = [items]
            
        if not items:
            print("No items found.")
            return None
            
        # 정확히 이름이 일치하는지 확인하거나 첫 번째 항목 반환
        for item in items:
            if item.get('yadmNm') == hospital_name:
                found_ykiho = item.get('ykiho')
                print(f"Found EXACT match! ykiho: {found_ykiho}")
                return found_ykiho
        
        # 정확한 일치가 없으면 첫 번째 것 반환 (유사도)
        first_ykiho = items[0].get('ykiho')
        print(f"No exact match, returning first result: {items[0].get('yadmNm')} -> {first_ykiho}")
        return first_ykiho

    except Exception as e:
        print(f"Exception happened: {e}")
        return None

if __name__ == "__main__":
    # 테스트용
    target = "동탄아이엠유의원"
    ykiho = get_ykiho(target)
    if ykiho:
        print(f"Final Result: {ykiho}")
    else:
        print("Failed to get ykiho.")
