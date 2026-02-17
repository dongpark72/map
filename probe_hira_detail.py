import requests
import json
import urllib.parse

# Using the working Hex Key
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

# Step 1: Get YKIHO for a sample hospital
BASIS_URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
HOSPITAL_NAME = "삼성서울병원"

def get_ankiho():
    params = {
        'serviceKey': KEY,
        'pageNo': '1',
        'numOfRows': '1',
        '_type': 'json',
        'yadmNm': HOSPITAL_NAME
    }
    try:
        res = requests.get(BASIS_URL, params=params, timeout=10)
        data = res.json()
        item = data['response']['body']['items']['item']
        if isinstance(item, list): item = item[0]
        ykiho = item.get('ykiho')
        print(f"Got ykiho: {ykiho}")
        return ykiho
    except Exception as e:
        print(f"Failed to get ykiho: {e}")
        return None

# Step 2: Probe Detail Info Service
# Service: MadmDtlInfoService2.7
# Operation: getDtlInfo2.7 ? or getDtlInfo ?
# Common operations:
# - getDtlInfo: 상세정보 (진료과목, 시설 등 개괄?) -> actually getMdlrtSbjectInfo is subjects.
# Let's try likely candidates for "Detailed Info"

def probe_detail(ykiho):
    base_url = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/"
    
    # Candidate operations
    ops = [
        "getDtlInfo2.7", 
        "getDtlInfo", 
        "getMdlrtSbjectInfo2.7", # 진료과목
        "getSpclMdlrtInfo2.7",   # 특수진료
        "getFacilityInfo2.7"     # 시설정보 (This matches getEqpInfo mostly?)
    ]
    
    for op in ops:
        url = base_url + op
        print(f"\n--- Testing Operation: {op} ---")
        params = {
            'serviceKey': KEY,
            '_type': 'json',
            'ykiho': ykiho,
            'numOfRows': 10,
            'pageNo': 1
        }
        
        try:
            res = requests.get(url, params=params, verify=False, timeout=10)
            print(f"Status: {res.status_code}")
            if res.status_code == 200:
                try:
                    data = res.json()
                    print("Response JSON:")
                    # Print first item/keys to see content
                    try:
                        items = data['response']['body']['items']
                        if items:
                            item = items['item']
                            if isinstance(item, list):
                                print(json.dumps(item[0], indent=2, ensure_ascii=False))
                            else:
                                print(json.dumps(item, indent=2, ensure_ascii=False))
                        else:
                            print("Empty items")
                    except KeyError:
                         print(res.text[:300])
                except:
                    print(res.text[:300])
            else:
                print(res.text[:200])
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    ykiho = get_ankiho()
    if ykiho:
        probe_detail(ykiho)
