import requests
import urllib.parse

keys = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"

def run_test(name, target_url, key, key_desc, extra_params=""):
    print(f"\n--- Testing {name} with {key_desc} ---")
    
    # 1. Try with QUOTED key (standard practice in code)
    enc_key = urllib.parse.quote(key)
    query_quoted = f"{target_url}^serviceKey={enc_key}{extra_params}"
    
    print(f"Query (Quoted Key): {query_quoted[:100]}...")
    try:
        res = requests.get(connector_url, params={'url': query_quoted}, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Body Len: {len(res.text)}")
        print(f"Body: {repr(res.text[:500])}")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Try with RAW key (if key has no special chars that break Connector syntax)
    # Connector syntax: ^ and | are delimiters. = is separator.
    # Key 1 has ==. It SHOULD be fine as value?
    if "==" in key:
        print(f"Query (Raw Key): Testing skipped (risk of breaking syntax?) Let's try...")
        query_raw = f"{target_url}^serviceKey={key}{extra_params}"
        try:
            res = requests.get(connector_url, params={'url': query_raw}, timeout=10)
            print(f"Status: {res.status_code}")
            print(f"Body Len: {len(res.text)}")
            print(f"Body: {repr(res.text[:500])}")
        except Exception as e:
            print(f"Error: {e}")

def test_hira(key, key_desc):
    url = "http://apis.data.go.kr/B551182/hiraInfoService/getHospBasisList"
    # Removing _type=json to see if XML works better (api supports both?)
    # HIRA basis usually supports default XML.
    params = "|numOfRows=1|pageNo=1"
    run_test("HIRA Basis", url, key, key_desc, params)

def test_real_price(key, key_desc):
    url = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"
    # Real Price needs LAWD_CD and DEAL_YMD
    params = "|LAWD_CD=11110|DEAL_YMD=202401|numOfRows=1"
    run_test("Real Price", url, key, key_desc, params)

print("=== STARTING REFINED CONNECTOR TESTS ===")
for i, key in enumerate(keys):
    desc = f"Key {i+1}"
    test_hira(key, desc)
    test_real_price(key, desc)
