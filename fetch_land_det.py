import requests
import time

def fetch_land():
    pnu = "2671025028100080001"
    url = "https://www.eum.go.kr/web/ar/lu/luLandDet.jsp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        print("Visiting Main...")
        session.get('https://www.eum.go.kr/web/am/amMain.jsp', timeout=10)
        time.sleep(1)
        
        print(f"Fetching {url}...")
        res = session.get(url, params={'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}, timeout=15)
        
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            with open('dump_land_det.html', 'w', encoding='utf-8') as f:
                f.write(res.text)
            print("Saved to dump_land_det.html")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_land()
