import requests
import xml.etree.ElementTree as ET

pnu = "1111013700100480000"
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
ned_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"

query_val = f"{ned_url}^key={ned_key}|pnu={pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=100"
res = session.get(connector_url, params={'url': query_val}, timeout=10)
if res.status_code == 200:
    root = ET.fromstring(res.text)
    for field in root.findall('.//field'):
        year = field.find('stdrYear').text
        if year == '2022':
            price = field.find('pblntfPclnd').text
            print(f"Year 2022 Price: {price}")
        if year == '2025':
            price = field.find('pblntfPclnd').text
            print(f"Year 2025 Price: {price}")
