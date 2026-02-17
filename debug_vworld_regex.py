import requests
import xml.etree.ElementTree as ET

pnu = "1111013400101100000"
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
ned_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"
query = f"{ned_url}^key={ned_key}|pnu={pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=5"
try:
    res = requests.get(connector_url, params={'url': query}, timeout=15)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        print("Response received")
        # Find all fields
        import re
        all_fields = re.findall(r'<field>(.*?)</field>', res.text, re.S)
        print(f"Fields found: {len(all_fields)}")
        for f_text in all_fields[:1]:
            year = re.search(r'<stdrYear>(.*?)</stdrYear>', f_text)
            z1 = re.search(r'<prposArea1Nm>(.*?)</prposArea1Nm>', f_text)
            z2 = re.search(r'<prposArea2Nm>(.*?)</prposArea2Nm>', f_text)
            print(f"Year: {year.group(1) if year else 'N/A'}")
            print(f"Z1: {z1.group(1) if z1 else 'N/A'}")
            print(f"Z2: {z2.group(1) if z2 else 'N/A'}")
except Exception as e:
    print(f"Error: {e}")
