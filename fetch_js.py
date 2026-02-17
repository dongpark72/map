import requests

url = "https://www.eum.go.kr/web/js/ar/lu/luLandDet.js"

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

res = session.get(url, timeout=10)
if res.status_code == 200:
    with open("e:/Antigravity/Gundammap/luLandDet.js", "w", encoding='utf-8') as f:
        f.write(res.text)
    print("Saved luLandDet.js")
else:
    print(f"Error: {res.status_code}")
