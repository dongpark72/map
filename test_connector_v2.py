import requests

def test_connector():
    url_recap = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
    url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
    key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://www.eum.go.kr/',
    }

    scenarios = [
        ("Original PNU Title", url_title, "26710", "25028"),
        ("Original PNU Recap", url_recap, "26710", "25028"),
        ("New PNU Title", url_title, "26710", "34027"),
        ("New PNU Recap", url_recap, "26710", "34027"),
    ]
    
    for name, api_url, sigungu, bjdong in scenarios:
        params_str = (
            f"url={api_url}^serviceKey={key}|sigunguCd={sigungu}|bjdongCd={bjdong}"
            f"|platGbCd=0|bun=0008|ji=0001|startDate=|endDate=|numOfRows=10|pageNo=1"
        )
        full_url = f"{connector_url}?{params_str}"
        try:
            print(f"Testing {name}...")
            res = requests.get(full_url, headers=headers, timeout=5)
            if "<totalCount>0</totalCount>" in res.text:
                print(f"  -> No Data")
            elif "<totalCount>" in res.text:
                import re
                m = re.search(r"<totalCount>(\d+)</totalCount>", res.text)
                count = m.group(1) if m else "?"
                print(f"  -> Found Data! Count: {count}")
                print(res.text[:300])
            else:
                print(f"  -> Unexpected response: {res.text[:100]}")
        except Exception as e:
            print(f"  -> Error: {e}")

if __name__ == "__main__":
    test_connector()
