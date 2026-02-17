import requests
import xml.etree.ElementTree as ET

pnu = "1111013400101100000"
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
ned_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"
query = f"{ned_url}^key={ned_key}|pnu={pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=5"
res = requests.get(connector_url, params={'url': query}, timeout=10)
print(f"Status: {res.status_code}")
# print(res.text)

if res.status_code == 200 and '<response>' in res.text:
    root = ET.fromstring(res.text)
    fields = root.findall('.//field')
    if fields:
        latest = fields[0]
        def get_v(e, t):
            n = e.find(t); return n.text.strip() if n is not None and n.text else ''
        print(f"Year: {get_v(latest, 'stdrYear')}")
        print(f"prposArea1Nm: {get_v(latest, 'prposArea1Nm')}")
        print(f"prposArea2Nm: {get_v(latest, 'prposArea2Nm')}")
        print(f"ladUseSittnNm: {get_v(latest, 'ladUseSittnNm')}")
