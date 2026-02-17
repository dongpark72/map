import requests
import xml.etree.ElementTree as ET

pnu = "1111013700100480000"
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
})

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
ned_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"

query_val = f"{ned_url}^key={ned_key}|pnu={pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=100"
res = session.get(connector_url, params={'url': query_val}, timeout=10)
if res.status_code == 200:
    root = ET.fromstring(res.text)
    fields = root.findall('.//field')
    data = []
    for f in fields:
        y = f.find('stdrYear').text if f.find('stdrYear') is not None else '?'
        p = f.find('pblntfPclnd').text if f.find('pblntfPclnd') is not None else '?'
        data.append((y, p))
    
    # Filter for 2022-2025
    target_years = ['2025', '2024', '2023', '2022']
    res_data = [d for d in data if d[0] in target_years]
    print(res_data)
