import requests
from bs4 import BeautifulSoup

def debug_eum():
    pnu = "2671025028100080001" # 부산 기장군 일광읍 신평리 8-1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Checking data for PNU: {pnu}")
    
    # 1. Gongsi (공시지가)
    print("\n[1] Checking Gongsi (Price)...")
    url = "https://www.eum.go.kr/web/ar/lu/luGongsi.jsp"
    res = requests.post(url, data={'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}, headers=headers)
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.select('table.board_list tbody tr')
        print(f"Found {len(rows)} price rows")
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                year = cols[0].get_text(strip=True)
                price = cols[1].get_text(strip=True)
                print(f"Year: {year}, Price: {price}")
    else:
        print("Failed to fetch Gongsi")

    # 2. Building Info
    print("\n[2] Checking Building Info...")
    url = "https://www.eum.go.kr/web/ar/lu/luBuildInfo.jsp"
    res = requests.post(url, data={'pnu': pnu}, headers=headers)
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # Check specific fields requested
        fields = ['건물명', '동명칭', '주용도', '대지면적', '연면적', '높이', '건폐율', '용적률']
        
        # Try to find the table cells
        for th in soup.find_all('th'):
            name = th.get_text(strip=True)
            td = th.find_next_sibling('td')
            if td:
                val = td.get_text(strip=True)
                if any(f in name for f in fields):
                    print(f"{name}: {val}")
    else:
        print("Failed to fetch Building Info")

if __name__ == "__main__":
    debug_eum()
