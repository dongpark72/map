import requests
import xml.etree.ElementTree as ET

pnu = "1111013700100480000"
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
ned_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"

query_val = f"{ned_url}^key={ned_key}|pnu={pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=50"
res = session.get(connector_url, params={'url': query_val}, timeout=10)
if res.status_code == 200:
    root = ET.fromstring(res.text)
    latest = root.findall('.//field')[0] # Usually the first one if we don't sort, but let's see.
    # Actually, let's find the latest (2025 if possible)
    fields = root.findall('.//field')
    fields.sort(key=lambda x: x.find('stdrYear').text if x.find('stdrYear') is not None else '0', reverse=True)
    latest = fields[0]
    
    print(f"Year: {latest.find('stdrYear').text}")
    print(f"Shape (tpgrphFrmCodeNm): {latest.find('tpgrphFrmCodeNm').text}")
    print(f"Terrain (tpgrphHgCodeNm): {latest.find('tpgrphHgCodeNm').text}")
    print(f"Price (pblntfPclnd): {latest.find('pblntfPclnd').text}")
