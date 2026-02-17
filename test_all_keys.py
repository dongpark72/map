import requests
import urllib.parse
import os

keys = []
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if 'PUBLIC_DATA_KEY' in line:
                keys.append(line.split('=')[1].strip().strip("'").strip('"'))

def test_all_combinations():
    url = 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    sigungu = "26470"
    month = "202411"
    
    for i, key in enumerate(keys):
        print(f"\n--- Testing Key {i+1} ---")
        
        # Method 1: Using requests params (requests handles encoding)
        try:
            res = requests.get(url, params={'serviceKey': key, 'LAWD_CD': sigungu, 'DEAL_YMD': month}, timeout=5)
            print(f"Method 1 (Params): Status {res.status_code}, Snippet: {res.text[:100].strip()}")
        except Exception as e: print(f"Method 1 fail: {e}")
        
        # Method 2: Manual URL with quoted key
        try:
            enc_key = urllib.parse.quote(key)
            full_url = f"{url}?serviceKey={enc_key}&LAWD_CD={sigungu}&DEAL_YMD={month}"
            res = requests.get(full_url, timeout=5)
            print(f"Method 2 (Manual Enc): Status {res.status_code}, Snippet: {res.text[:100].strip()}")
        except Exception as e: print(f"Method 2 fail: {e}")

        # Method 3: Manual URL with raw key (dangerous if key has special chars)
        try:
            full_url = f"{url}?serviceKey={key}&LAWD_CD={sigungu}&DEAL_YMD={month}"
            res = requests.get(full_url, timeout=5)
            print(f"Method 3 (Manual Raw): Status {res.status_code}, Snippet: {res.text[:100].strip()}")
        except Exception as e: print(f"Method 3 fail: {e}")

if __name__ == "__main__":
    test_all_combinations()
