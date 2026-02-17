import requests
from bs4 import BeautifulSoup

pnu = "1111013700100480000"
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/ar/lu/luLandDet.jsp'
})

url = "https://www.eum.go.kr/web/ar/lu/luLandDetYearAjax.jsp"
params = {"pnu": pnu}

res = session.get(url, params=params, timeout=10)
print(f"Status: {res.status_code}")
if res.status_code == 200:
    print("--- AJAX Response ---")
    print(res.text)
    
    soup = BeautifulSoup(res.text, 'html.parser')
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) >= 2:
            print(f"Year: {tds[0].get_text(strip=True)}, Price: {tds[1].get_text(strip=True)}")
else:
    print(f"Error: {res.status_code}")
