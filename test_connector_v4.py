import requests

def test_connector():
    url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
    key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://www.eum.go.kr/',
    }

    # Query broadly
    params_str = (
        f"url={url_title}^serviceKey={key}|sigunguCd=26710|bjdongCd=25028"
        f"|numOfRows=1|pageNo=1"
    )
    full_url = f"{connector_url}?{params_str}"
    
    print("Testing broad query...")
    try:
        res = requests.get(full_url, headers=headers, timeout=5)
        print(res.text[:300])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connector()
