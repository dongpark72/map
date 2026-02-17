import requests
from bs4 import BeautifulSoup

def debug_eum_session():
    pnu = "2671025028100080001"
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp',
        'Origin': 'https://www.eum.go.kr',
        'Host': 'www.eum.go.kr'
    }
    
    print("1. Visiting Main Page...")
    try:
        main_url = "https://www.eum.go.kr/web/am/amMain.jsp"
        main_res = session.get(main_url, headers=headers, timeout=10)
        print(f"Main Page Status: {main_res.status_code}")
        print("Cookies:", session.cookies.get_dict())
    except Exception as e:
        print(f"Main Page Error: {e}")
        return

    print("\n2. Fetching Land Detail (luLandDet.jsp)...")
    url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
    params = {'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}
    
    try:
        res = session.get(url, params=params, headers=headers, timeout=10)
        print(f"Land Detail Status: {res.status_code}")
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            print("Title:", soup.title.string if soup.title else "No Title")
            # Check price/area
            for td in soup.find_all('td'):
                if '㎡' in td.get_text():
                    print("Found Area:", td.get_text(strip=True))
                    break
    except Exception as e:
        print(f"Land Detail Error: {e}")

    print("\n3. Fetching Gongsi (luGongsi.jsp)...")
    url = "https://www.eum.go.kr/web/ar/lu/luGongsi.jsp"
    try:
        res = session.get(url, params=params, headers=headers, timeout=10)
        print(f"Gongsi Status: {res.status_code}")
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            rows = soup.select('table tbody tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    print(f"Year: {cols[0].get_text(strip=True)}, Price: {cols[1].get_text(strip=True)}")
    except Exception as e:
        print(f"Gongsi Error: {e}")

if __name__ == "__main__":
    debug_eum_session()
