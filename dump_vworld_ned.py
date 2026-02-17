import requests

def fetch_and_save():
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    target_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
    key = "98A53FD9-F542-32C4-9589-78A54E531AF7"
    pnu = "2671025028100080001"
    
    query_val = f"{target_url}^key={key}|pnu={pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=10"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://www.eum.go.kr/'
    }
    
    res = requests.get(connector_url, params={'url': query_val}, headers=headers)
    with open('vworld_ned.xml', 'w', encoding='utf-8') as f:
        f.write(res.text)
    print("Saved vworld_ned.xml")

if __name__ == "__main__":
    fetch_and_save()
