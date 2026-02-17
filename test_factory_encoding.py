import requests
import urllib.parse

# API configuration - Try both keys
API_KEYS = [
    'YfL0bnXWkWTqsOkJLDNjmPyFMJvZHjXxnQVBNvDjVZdMoMQRJLSNmNdEqFJWOzSIXdBvvOoJLRGxpMQRVMVOBw==',
    'YfL0bnXWkWTqsOkJLDNjmPyFMJvZHjXxnQVBNvDjVZdMoMQRJLSNmNdEqFJWOzSIXdBvvOoJLRGxpMQRVMVOBw%3D%3D'
]
SIGUNGU_CD = '26530'  # Busan Sasang-gu
API_URL = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'

# Test with recent month
test_month = '202502'

print("Testing Factory/Warehouse API with different key encodings")
print("=" * 80)

for idx, api_key in enumerate(API_KEYS, 1):
    print(f"\n[Test {idx}] API Key: {api_key[:50]}...")
    
    params = {
        'serviceKey': api_key,
        'LAWD_CD': SIGUNGU_CD,
        'DEAL_YMD': test_month,
        'numOfRows': '100',
        'pageNo': '1'
    }
    
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        res = session.get(API_URL, params=params, timeout=10)
        
        print(f"Status Code: {res.status_code}")
        print(f"Response Length: {len(res.text)} bytes")
        
        if res.status_code == 200:
            print(f"Response Preview (first 500 chars):")
            print(res.text[:500])
            
            if "<item>" in res.text:
                print("\n*** DATA FOUND! ***")
                with open(f'factory_success_{test_month}.xml', 'w', encoding='utf-8') as f:
                    f.write(res.text)
                print(f"Saved to: factory_success_{test_month}.xml")
                break
            elif "<items/>" in res.text or "<items />" in res.text:
                print("No data for this period (empty items)")
            else:
                print("Unknown response format")
        else:
            print(f"Error Response: {res.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

print("\n" + "=" * 80)
print("Test completed")
