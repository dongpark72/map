import requests

def test_connector():
    # PNU: 2671025028100080001 (Busan Gijang...)
    # Sigungu: 26710
    # Bjdong: 25028
    # 1000(Land/San) -> 1 -> platGbCd=0
    # Bun: 0008
    # Ji: 0001
    
    target_url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
    key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
    
    # Construct the weird parameter string for UrlConnector.jsp
    # format: ?url=TARGET^serviceKey=KEY|sigunguCd=...
    
    # Note: Requests params dict automatically URL-encodes values.
    # But the connector expects `^` and `|` which might need careful handling.
    # I'll construct the query string manually to be safe or pass as string.
    
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    params_str = (
        f"url={target_url}^serviceKey={key}|sigunguCd=26710|bjdongCd=25028"
        f"|platGbCd=0|bun=0008|ji=0001|startDate=|endDate=|numOfRows=10|pageNo=1"
    )
    
    print(f"Requesting: {connector_url}?{params_str}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://www.eum.go.kr/',
        'Accept': 'text/xml,application/xml'
    }
    
    try:
        res = requests.get(connector_url, params=params_str, headers=headers)
        # Note: passing params as string is not supported by requests directly in 'params' kwarg usually?
        # Requests 'params' takes dict or bytes. If string intermixed, it might be double encoded.
        # Let's use direct URL construction.
        
        full_url = f"{connector_url}?{params_str}"
        res = requests.get(full_url, headers=headers)
        
        print(f"Status: {res.status_code}")
        print(res.text[:500])
        
        with open("connector_result.xml", "w", encoding="utf-8") as f:
            f.write(res.text)
            
    except Exception as e:
        print(e)

if __name__ == "__main__":
    test_connector()
