import requests
import urllib.parse
import json

def test_hira_detail_fixed():
    # Test Data
    hospital_name = "연세로의료의원" # From user screenshot
    api_key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    enc_key = urllib.parse.quote(api_key)
    enc_hosp = urllib.parse.quote(hospital_name)
    
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    basis_url = "http://apis.data.go.kr/B551182/hiraInfoService/getHospBasisList"
    
    print(f"Testing HIRA Basis for: {hospital_name}")
    q_basis = f"{basis_url}^serviceKey={enc_key}|_type=json|yadmNm={enc_hosp}|numOfRows=1|pageNo=1"
    
    try:
        res = requests.get(connector_url, params={'url': q_basis}, timeout=10)
        print(f"Status: {res.status_code}")
        try:
            data = res.json()
            items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
        except json.JSONDecodeError:
            print("Failed to parse JSON. Raw response:")
            print(res.text[:1000])
            return
        
        if items:
            print("Successfully found hospital info!")
            print(json.dumps(items, indent=2, ensure_ascii=False))
            
            # Test Step 2
            ykiho = items[0].get('ykiho') if isinstance(items, list) else items.get('ykiho')
            if ykiho:
                print(f"\nTesting HIRA Detail for ykiho: {ykiho}")
                detail_url = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7"
                q_detail = f"{detail_url}^serviceKey={enc_key}|_type=json|ykiho={ykiho}|numOfRows=1|pageNo=1"
                res_det = requests.get(connector_url, params={'url': q_detail}, timeout=10)
                print(f"Detail Status: {res_det.status_code}")
                print(f"Detail Body: {res_det.text[:300]}")
        else:
            print("Hospital not found.")
            print(f"Raw Response: {res.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hira_detail_fixed()
