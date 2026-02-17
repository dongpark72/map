import requests
import os
import urllib.parse

PUBLIC_DATA_KEY = ""
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if 'PUBLIC_DATA_KEY_1' in line:
                PUBLIC_DATA_KEY = line.split('=')[1].strip().strip("'").strip('"')

def check_apt_connector():
    url = 'http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev'
    connector = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    enc_key = urllib.parse.quote(PUBLIC_DATA_KEY)
    query = f"{url}^serviceKey={enc_key}|LAWD_CD=26470|DEAL_YMD=202511"
    
    res = requests.get(connector, params={'url': query}, timeout=10)
    print(f"Status: {res.status_code}")
    print(f"Response snippet: {res.text[:500]}")

if __name__ == "__main__":
    check_apt_connector()
