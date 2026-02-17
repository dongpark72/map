import requests
from bs4 import BeautifulSoup
import os

def dump_eum():
    pnu = "2671025028100080001" # 부산 기장군 일광읍 신평리 8-1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Dumping data for PNU: {pnu}")
    
    # Building Info
    print("\n[2] Dumping Building Info...")
    url = "https://www.eum.go.kr/web/ar/lu/luBuildInfo.jsp"
    # Using POST as in the debug script, but views.py uses GET usually?
    # views.py uses session.get(url, params=params). params has 'pnu', 'mode', 'isNoScr'.
    # I should match views.py exactly.
    
    params = {
        'pnu': pnu,
        'mode': 'search',
        'isNoScr': 'script'
    }
    
    # Create session to match views.py
    session = requests.Session()
    session.headers.update(headers)
    
    # 1. Visit Main to set cookies
    print("Visiting Main...")
    session.get("https://www.eum.go.kr/web/am/amMain.jsp")
    
    print("Fetching BuildInfo...")
    res = session.get(url, params=params)
    
    if res.status_code == 200:
        with open("dump_build_info.html", "w", encoding="utf-8") as f:
            f.write(res.text)
        print("Saved to dump_build_info.html")
    else:
        print(f"Failed: {res.status_code}")

if __name__ == "__main__":
    dump_eum()
