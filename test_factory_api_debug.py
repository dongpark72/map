import requests
import urllib.parse

# API configuration
API_KEY = 'YfL0bnXWkWTqsOkJLDNjmPyFMJvZHjXxnQVBNvDjVZdMoMQRJLSNmNdEqFJWOzSIXdBvvOoJLRGxpMQRVMVOBw=='
SIGUNGU_CD = '26530'  # Busan Sasang-gu
API_URL = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
CONNECTOR_URL = 'https://www.eum.go.kr/dataapis/UrlConnector.jsp'

# Test with recent months
test_months = ['202601', '202512', '202511', '202502']

print("Testing Factory/Warehouse API for Sasang-gu")
print("=" * 80)

for month in test_months:
    print(f"\n[{month}]")
    enc_key = urllib.parse.quote(API_KEY)
    query = f"{API_URL}^serviceKey={enc_key}|LAWD_CD={SIGUNGU_CD}|DEAL_YMD={month}"
    
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        res = session.get(CONNECTOR_URL, params={'url': query}, timeout=10)
        
        print(f"Status Code: {res.status_code}")
        print(f"Response Length: {len(res.text)} bytes")
        print(f"Response Content (first 500 chars):")
        print(res.text[:500])
        print("-" * 80)
        
        # Save full response to file for inspection
        with open(f'factory_response_{month}.xml', 'w', encoding='utf-8') as f:
            f.write(res.text)
        print(f"Full response saved to: factory_response_{month}.xml")
            
    except Exception as e:
        print(f"Exception: {e}")

print("\n" + "=" * 80)
print("Test completed. Check the XML files for full responses.")
