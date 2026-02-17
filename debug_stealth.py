
import requests
import urllib.request
import ssl

URL = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

# Headers that look exactly like Chrome
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive',
    'Referer': 'http://www.onbid.co.kr/'
}

params = {
    'serviceKey': KEY,
    'pageNo': '1',
    'numOfRows': '10',
    'SIDO': '서울특별시',
    'SGK': '강남구',
    'DPSL_MTD_CD': '0002'
}

print("--- Test 1: requests with Full Headers ---")
try:
    r = requests.get(URL, params=params, headers=HEADERS, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Server: {r.headers.get('Server', '')}")
    print(f"Body start: {r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")

print("\n--- Test 2: urllib.request (Different underlying library) ---")
try:
    # Construct URL
    import urllib.parse
    qs = urllib.parse.urlencode(params, safe='=')
    full_url = f"{URL}?{qs}"
    
    req = urllib.request.Request(full_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as response:
        print(f"Status: {response.status}")
        print(f"Body start: {response.read().decode('utf-8')[:300]}")
except Exception as e:
    print(f"Error: {e}")
