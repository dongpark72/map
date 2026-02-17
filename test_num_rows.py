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

# Test with 10 rows vs 50 rows
def test_rows(n):
    print(f"\n--- Testing with numOfRows={n} ---")
    query_val = f"{ned_url}^key={ned_key}|pnu={pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows={n}"
    res = session.get(connector_url, params={'url': query_val}, timeout=10)
    if res.status_code == 200:
        root = ET.fromstring(res.text)
        fields = root.findall('.//field')
        print(f"Total fields returned: {len(fields)}")
        years = [f.find('stdrYear').text for f in fields if f.find('stdrYear') is not None]
        print(f"Years: {years}")

test_rows(10)
test_rows(50)
