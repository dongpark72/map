import requests
from bs4 import BeautifulSoup

def debug_eum():
    pnu = "2671025028100080001"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    params = {
        'pnu': pnu,
        'mode': 'search',
        'isNoScr': 'script'
    }
    
    print(f"Checking data for PNU: {pnu}")
    
    # 1. Gongsi (공시지가)
    print("\n[1] Checking Gongsi (Price)...")
    url = "https://www.eum.go.kr/web/ar/lu/luGongsi.jsp"
    try:
        res = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            rows = soup.select('table tbody tr')
            print(f"Found {len(rows)} rows")
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    year = cols[0].get_text(strip=True)
                    price = cols[1].get_text(strip=True)
                    print(f"Year: {year}, Price: {price}")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Building Info
    print("\n[2] Checking Building Info...")
    url = "https://www.eum.go.kr/web/ar/lu/luBuildInfo.jsp"
    try:
        res = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # Simply print all th/td pairs to see what we get
            for th in soup.find_all('th'):
                td = th.find_next_sibling('td')
                if td:
                    print(f"{th.get_text(strip=True)}: {td.get_text(strip=True)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_eum()
