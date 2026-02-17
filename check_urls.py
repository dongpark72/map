import requests

def check_urls():
    pnu = "2671025028100080001"
    base_url = "https://www.eum.go.kr/web/ar/lu/"
    candidates = [
        "luBuild.jsp",
        "luBuilding.jsp",
        "luBldg.jsp",
        "luBldgInfo.jsp",
        "luBldRgst.jsp",
        "luBldReg.jsp",
        "luCons.jsp",
        "luConstruct.jsp",
        "luStrct.jsp",
        "luGongsi.jsp", # Checking again
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    session = requests.Session()
    # session.get("https://www.eum.go.kr/web/am/amMain.jsp", headers=headers)
    
    params = {'pnu': pnu, 'mode': 'search', 'isNoScr': 'script'}
    
    for c in candidates:
        url = base_url + c
        try:
            res = session.get(url, params=params, headers=headers, timeout=2)
            if res.status_code != 404:
                print(f"FOUND: {c} -> {res.status_code}")
            else:
                 # pass
                 print(f"404: {c}")
        except Exception as e:
            pass

if __name__ == "__main__":
    check_urls()
