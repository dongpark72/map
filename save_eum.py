import requests

pnu = "2671034027100080001"
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
params = {'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

res = requests.get(url, params=params, headers=headers)
with open("e:\\Gundammap\\eum_response.html", "w", encoding="utf-8") as f:
    f.write(res.text)
print(f"Saved response to eum_response.html. Length: {len(res.text)}")
