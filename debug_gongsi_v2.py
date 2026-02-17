import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json

# PNU for 서울시 종로구 우정국로 48 (Gyeonji-dong 48)
pnu = "1111013700100480000"

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
})

# 1. Check LuLandDet.jsp
print(f"--- Checking luLandDet.jsp for PNU: {pnu} ---")
url_det = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
res_det = session.get(url_det, params={"pnu": pnu}, timeout=10)
print(f"Status: {res_det.status_code}")
if res_det.status_code == 200:
    soup = BeautifulSoup(res_det.text, 'html.parser')
    # Look for anything related to price or gongsi
    gongsi_row = soup.find(lambda tag: tag.name == 'th' and '공시지가' in tag.get_text())
    if gongsi_row:
        print(f"Found Gongsi Header: {gongsi_row.get_text(strip=True)}")
        td = gongsi_row.find_next_sibling('td')
        if td:
            print(f"Gongsi Value: {td.get_text(strip=True)}")

# 2. Check V-World NED via Connector
print(f"--- Checking V-World NED via Connector for PNU: {pnu} ---")
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
ned_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"
query_val = f"{ned_url}^key={ned_key}|pnu={pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=10"
res_ned = session.get(connector_url, params={'url': query_val}, timeout=10)
print(f"Status: {res_ned.status_code}")
if res_ned.status_code == 200:
    print("NED XML Response Snapshot:")
    print(res_ned.text[:1000])
    try:
        root = ET.fromstring(res_ned.text)
        for field in root.findall('.//field'):
            year = field.find('stdrYear').text if field.find('stdrYear') is not None else '?'
            price = field.find('pblntfPclnd').text if field.find('pblntfPclnd') is not None else '?'
            print(f"NED: Year={year}, Price={price}")
    except Exception as e:
        print(f"XML Parse Error: {e}")
