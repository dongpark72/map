import requests
import time

def check_eum_scrape():
    # S&S Building PNU
    pnu = "1111012900100680005" 
    
    url = f"https://www.eum.go.kr/web/am/amMain.jsp?action=search&pnu={pnu}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print("Fetching Eum Main Page...")
    start = time.time()
    try:
        res = requests.get(url, headers=headers, timeout=10)
        end = time.time()
        print(f"Status: {res.status_code}")
        print(f"Time: {end - start:.4f} sec")
        
        if "층별현황" in res.text or "지상" in res.text:
             print("Found keywords in HTML.")
        else:
             print("Keywords NOT found in main HTML (Might be loaded via AJAX).")
             
        # Eum typically loads building info via AJAX. 
        # Let's try to guess the AJAX endpoint. 
        # Often: /web/am/amBld* 
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_eum_scrape()
