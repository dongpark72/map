import requests

def test_vworld_ned():
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # URL and Key found in eum source
    target_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
    key = "98A53FD9-F542-32C4-9589-78A54E531AF7"
    pnu = "2671025028100080001"
    
    # query string for connector
    query_val = f"{target_url}^key={key}|pnu={pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=10"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://www.eum.go.kr/'
    }
    
    print(f"Requesting V-World NED via Connector...")
    try:
        res = requests.get(connector_url, params={'url': query_val}, headers=headers, timeout=10)
        print(f"Status: {res.status_code}")
        print(res.text[:500])
        
        if "<totalCount>0</totalCount>" in res.text:
            print("No Data Found.")
        else:
             print("Data Found!")
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_vworld_ned()
