
import requests
import urllib.parse

# Switch to HTTPS
url = "https://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
key_dec = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("Testing HTTPS Minimal...")
try:
    # Just page params
    params = {
        'serviceKey': key_dec,
        'pageNo': '1',
        'numOfRows': '10'
    }
    r = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Body: {r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")
