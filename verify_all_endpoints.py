import requests

def test_endpoints():
    base_url = "http://175.126.187.59:8000"
    endpoints = [
        "/",
        "/proxy/landinfo/?pnu=2620012100103180045",
        "/proxy/building-detail/?pnu=2620012100103180045",
        "/proxy/real-price/?sigunguCd=26200&bjdongCd=2620012100&type=land"
    ]
    
    for ep in endpoints:
        url = base_url + ep
        try:
            res = requests.get(url, timeout=10)
            print(f"{res.status_code} - {ep}")
        except Exception as e:
            print(f"FAIL - {ep} - {e}")

if __name__ == "__main__":
    test_endpoints()
