import requests
import urllib.parse

# API configuration
API_KEY = 'YfL0bnXWkWTqsOkJLDNjmPyFMJvZHjXxnQVBNvDjVZdMoMQRJLSNmNdEqFJWOzSIXdBvvOoJLRGxpMQRVMVOBw=='
SIGUNGU_CD = '26530'  # Busan Sasang-gu
API_URL = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'

# Test with recent month
test_month = '202502'

print("Testing Factory/Warehouse API DIRECTLY (without connector)")
print("=" * 80)

# Direct API call
params = {
    'serviceKey': API_KEY,
    'LAWD_CD': SIGUNGU_CD,
    'DEAL_YMD': test_month,
    'numOfRows': '100',
    'pageNo': '1'
}

try:
    print(f"\nDirect API Call for {test_month}")
    print(f"URL: {API_URL}")
    print(f"Params: LAWD_CD={SIGUNGU_CD}, DEAL_YMD={test_month}")
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    res = session.get(API_URL, params=params, timeout=10)
    
    print(f"\nStatus Code: {res.status_code}")
    print(f"Response Length: {len(res.text)} bytes")
    print(f"\nFull Response:")
    print(res.text)
    
    # Save to file
    with open(f'factory_direct_{test_month}.xml', 'w', encoding='utf-8') as f:
        f.write(res.text)
    print(f"\nSaved to: factory_direct_{test_month}.xml")
        
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
