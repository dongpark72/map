import requests
import json

# Hex Key (Known working)
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
YKIHO = 'JDQ4MTg4MSM1MSMkMSMkMCMkODkkMzgxMzUxIzExIyQxIyQzIyQ3OSQyNjE4MzIjNDEjJDEjJDYjJDgz' # Samsung Seoul Hospital

def probe_correct_endpoints():
    base_urls = [
        "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/",
        "http://apis.data.go.kr/B551182/MadmDtlInfoService2.7/"
    ]
    
    # Operation names to test
    ops = [
        "getDtlInfo",       # Standard naming
        "getDtlInfo2.7",    # Versioned naming
        "getHospDtlInfo",   # Possible alt
        "getHospDtlInfo2.7"
    ]

    for base in base_urls:
        for op in ops:
            url = base + op
            print(f"Testing: {url}")
            params = {
                'serviceKey': KEY,
                '_type': 'json',
                'ykiho': YKIHO
            }
            try:
                res = requests.get(url, params=params, verify=False, timeout=5)
                if res.status_code == 200:
                    try:
                        data = res.json()
                        items = data.get('response', {}).get('body', {}).get('items')
                        if items:
                            print(f"!!! FOUND SUCCESS: {url}")
                            print(json.dumps(items, indent=2, ensure_ascii=False))
                            return
                        else:
                            print(f"  200 OK but empty items.")
                    except:
                        print(f"  200 OK but parse error or not JSON.")
                else:
                    print(f"  Status: {res.status_code}")
            except Exception as e:
                print(f"  Error: {e}")

if __name__ == "__main__":
    probe_correct_endpoints()
