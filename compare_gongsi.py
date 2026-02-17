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
    query_val = f"{ned_url}^key={ned_key}|pnu={pnu_val}|domain=http://www.eum.go.kr|format=xml|numOfRows=10"
    res_ned = session.get(connector_url, params={'url': query_val}, timeout=10)
    
    if res_ned.status_code == 200:
        try:
            root = ET.fromstring(res_ned.text)
            years = []
            for field in root.findall('.//field'):
                year = field.find('stdrYear').text if field.find('stdrYear') is not None else '?'
                price = field.find('pblntfPclnd').text if field.find('pblntfPclnd') is not None else '?'
                years.append(f"{year}: {price}")
            print(f"NED Years: {', '.join(years)}")
        except:
             print("NED Parse Error")
    else:
        print(f"NED Status: {res_ned.status_code}")

    # LuGongsi.jsp Check
    gongsi_url = "https://www.eum.go.kr/web/ar/lu/luGongsi.jsp"
    res_gongsi = session.get(gongsi_url, params={"pnu": pnu_val}, timeout=10)
    print(f"LuGongsi Status: {res_gongsi.status_code}")
    if res_gongsi.status_code == 200:
        soup = BeautifulSoup(res_gongsi.text, 'html.parser')
        rows = []
        for tr in soup.find_all('tr'):
            tds = tr.find_all(['td', 'th'])
            if len(tds) >= 2:
                rows.append(f"{tds[0].get_text(strip=True)}: {tds[1].get_text(strip=True)}")
        print(f"LuGongsi Rows: {', '.join(rows)}")

check_pnu("2671025621100080001", "Ilwang-eup Sinpyeong-ri 8-1")
check_pnu("1111013700100480000", "Ujeongguk-ro 48")
