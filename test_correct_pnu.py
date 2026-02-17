import requests
import xml.etree.ElementTree as ET

pnu = "1111012900100680005"
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
ned_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"

def test_pnu(target_pnu, n):
    print(f"\n--- Testing PNU {target_pnu} with numOfRows={n} ---")
    query_val = f"{ned_url}^key={ned_key}|pnu={target_pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows={n}"
    res = session.get(connector_url, params={'url': query_val}, timeout=10)
    if res.status_code == 200:
        root = ET.fromstring(res.text)
        fields = root.findall('.//field')
        years = []
        for f in fields:
            y = f.find('stdrYear').text if f.find('stdrYear') is not None else '?'
            years.append(y)
        print(f"Total: {len(fields)}, Years: {years}")

test_pnu(pnu, 10)
test_pnu(pnu, 50)
