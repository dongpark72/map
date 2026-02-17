import requests
from bs4 import BeautifulSoup

pnu = "1111013700100480000"
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/ar/lu/luLandDet.jsp'
})

# First access luLandDet.jsp to get cookies
session.get("https://www.eum.go.kr/web/ar/lu/luLandDet.jsp", params={"pnu": pnu})

# Now access luGongsi.jsp
res = session.get("https://www.eum.go.kr/web/ar/lu/luGongsi.jsp", params={"pnu": pnu})
print(f"Status: {res.status_code}")
if res.status_code == 200:
    print(res.text[:1000])
else:
    # Try different path
    res2 = session.get("https://www.eum.go.kr/web/ar/lu/luGongsiDet.jsp", params={"pnu": pnu})
    print(f"Status Det: {res2.status_code}")
