
import requests

url1 = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
url2 = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getThingInfoList"

key = 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def test_url(u, name):
    print(f"Testing {name}...")
    try:
        params = {
            'serviceKey': key,
            'pageNo': 1, 
            'numOfRows': 10
        }
        r = requests.get(u, params=params, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text[:300]}")
    except Exception as e:
        print(e)

test_url(url1, "getUnifyUsageCltr (Original)")
test_url(url2, "getThingInfoList (Alternative)")
