import requests
from bs4 import BeautifulSoup
import re

pnu = "2644010100107900000"
url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
}

res = requests.get(url, params={'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

# Search for any text containing '동' or building related info
print("--- Searching for building info in HTML ---")
for tag in soup.find_all(['td', 'th', 'div']):
    text = tag.get_text(strip=True)
    if '동' in text and len(text) < 50:
        print(f"Tag: {tag.name}, Text: {text}")

# Check if there is a '건축물대장' link or similar
links = soup.find_all('a')
for link in links:
    if '건축물' in link.get_text():
        print(f"Link found: {link.get_text()} -> {link.get('href')}")
