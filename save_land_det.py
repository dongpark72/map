import requests

pnu = "1111013700100480000"
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

res = session.get(url, params={"pnu": pnu}, timeout=10)
if res.status_code == 200:
    with open("e:/Antigravity/Gundammap/land_det_debug.html", "w", encoding='utf-8') as f:
        f.write(res.text)
    print("Saved luLandDet.jsp to land_det_debug.html")
else:
    print(f"Error: {res.status_code}")
