import requests
import urllib.parse
import json
import xml.etree.ElementTree as ET

# API Keys from .env or views.py
PUBLIC_DATA_KEYS = [
    'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
    'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
]

def debug_hira_workflow_v2():
    # Use the second key as it seems to be the one prioritized in code
    api_key = PUBLIC_DATA_KEYS[1]
    enc_key = urllib.parse.quote(api_key)
    
    # 1. Get Basis Info (to get ykiho)
    basis_url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    hospital_name = "동탄아이엠유의원" 
    
    print(f"--- Step 1: Getting Basis Info for {hospital_name} ---")
    q_basis = f"{basis_url}^serviceKey={enc_key}|_type=json|yadmNm={hospital_name}|numOfRows=1|pageNo=1"
    
    ykiho = None
    try:
        res = requests.get(connector_url, params={'url': q_basis}, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Raw Text (First 300 chars): {res.text[:300]}")
        
        try:
            data = res.json()
            print("Response is JSON.")
            items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            
            if isinstance(items, list) and len(items) > 0:
                basis_item = items[0]
            elif isinstance(items, dict):
                basis_item = items
            else:
                print("No items found in JSON.")
                basis_item = None

            if basis_item:
                ykiho = basis_item.get('ykiho')
                
        except json.JSONDecodeError:
            print("Response is NOT JSON. Trying XML...")
            try:
                root = ET.fromstring(res.text)
                items = root.findall('.//item')
                if items:
                    ykiho_el = items[0].find('ykiho')
                    if ykiho_el is not None:
                        ykiho = ykiho_el.text
                        print("Found ykiho in XML.")
                else:
                    print("No items found in XML.")
            except Exception as e:
                print(f"XML Parsing failed: {e}")
                
        print(f"Found ykiho: {ykiho}")
        
    except Exception as e:
        print(f"Step 1 Failed: {e}")
        return

    if not ykiho:
        print("Could not retrieve ykiho. Aborting Step 2.")
        return

    # 2. Get Detail Info (Facility Info)
    detail_url = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7"
    
    print(f"\n--- Step 2: Getting Facility Info for ykiho {ykiho} ---")
    q_detail = f"{detail_url}^serviceKey={enc_key}|_type=json|ykiho={ykiho}|numOfRows=1|pageNo=1"
    
    try:
        res = requests.get(connector_url, params={'url': q_detail}, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Raw Body:\n{res.text}")
        
    except Exception as e:
        print(f"Step 2 Failed: {e}")

if __name__ == "__main__":
    debug_hira_workflow_v2()
