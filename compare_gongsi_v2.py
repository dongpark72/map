import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json

def check_pnu(pnu_val, label):
    print(f"\n===== Checking {label} (PNU: {pnu_val}) =====")
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })

    # NED Check
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
    ned_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"
    query_val = f"{ned_url}^key={ned_key}|pnu={pnu_val}|domain=http://www.eum.go.kr|format=xml|numOfRows=20"
    res_ned = session.get(connector_url, params={'url': query_val}, timeout=10)
    
    if res_ned.status_code == 200:
        try:
            root = ET.fromstring(res_ned.text)
            years = {}
            for field in root.findall('.//field'):
                year = field.find('stdrYear').text if field.find('stdrYear') is not None else '?'
                price = field.find('pblntfPclnd').text if field.find('pblntfPclnd') is not None else '?'
                years[year] = price
            
            sorted_years = sorted(years.keys(), reverse=True)
            print(f"NED Data (Last 5 years): { {y: years[y] for y in sorted_years[:5]} }")
        except Exception as e:
             print(f"NED Parse Error: {e}")
    else:
        print(f"NED Status: {res_ned.status_code}")

check_pnu("2671025621100080001", "Ilwang-eup Sinpyeong-ri 8-1")
check_pnu("1111013700100480000", "Ujeongguk-ro 48")
