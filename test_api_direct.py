"""
공공데이터포털 API 직접 테스트 - 층별 정보 확인
"""
import requests
import xml.etree.ElementTree as ET
import urllib.parse
import sys

# Redirect output to file
output_file = open('api_test_result.txt', 'w', encoding='utf-8')
original_stdout = sys.stdout
sys.stdout = output_file

try:
    # 테스트할 건물 PK (로그에서 확인된 값)
    test_pk = "10311100190464"

    # API 설정
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    api_url_flr = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
    api_url_expos = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrExposPubuseAreaInfo"

    api_keys = [
        "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
        "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368",
    ]

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})

    print(f"Testing floor APIs for PK: {test_pk}")
    print("=" * 80)

    for key_idx, api_key in enumerate(api_keys):
        print(f"\n[API Key #{key_idx + 1}]")
        enc_key = urllib.parse.quote(api_key)
        
        # Test 1: getBrFlrOulnInfo
        print(f"\n1. getBrFlrOulnInfo (층별개요)")
        try:
            query = f"{api_url_flr}^serviceKey={enc_key}|numOfRows=300|mgmBldrgstPk={test_pk}"
            print(f"   Query: {query[:100]}...")
            
            response = session.get(connector_url, params={'url': query}, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response length: {len(response.text)} bytes")
            
            if response.status_code == 200:
                # Check for error messages
                if 'SERVICE_KEY_IS_NOT_REGISTERED_ERROR' in response.text:
                    print("   ❌ API Key not registered")
                elif 'NORMAL_SERVICE' in response.text or '<item>' in response.text:
                    root = ET.fromstring(response.text)
                    items = root.findall('.//item')
                    print(f"   ✓ Found {len(items)} floor records")
                    
                    if items:
                        # Show first item details
                        first = items[0]
                        print(f"\n   First floor record:")
                        for child in first:
                            if child.text and child.text.strip():
                                print(f"      {child.tag}: {child.text[:50]}")
                        
                        # Count by floor type
                        floor_types = {}
                        for item in items:
                            flr_gb = item.find('flrGbCdNm')
                            if flr_gb is not None and flr_gb.text:
                                floor_types[flr_gb.text] = floor_types.get(flr_gb.text, 0) + 1
                        print(f"\n   Floor distribution: {floor_types}")
                    else:
                        print("   ⚠️  Response OK but no items found")
                        # Show response snippet
                        print(f"\n   Response snippet:\n{response.text[:1000]}")
                else:
                    print("   ⚠️  Unknown response format")
                    print(f"\n   Response snippet:\n{response.text[:1000]}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except requests.Timeout:
            print("   ❌ Timeout - 서버 연결 시간 초과")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 2: getBrExposPubuseAreaInfo
        print(f"\n2. getBrExposPubuseAreaInfo (전유부분)")
        try:
            query = f"{api_url_expos}^serviceKey={enc_key}|numOfRows=300|mgmBldrgstPk={test_pk}"
            
            response = session.get(connector_url, params={'url': query}, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                if '<item>' in response.text:
                    root = ET.fromstring(response.text)
                    items = root.findall('.//item')
                    print(f"   ✓ Found {len(items)} records")
                else:
                    print("   ⚠️  No items found")
                    print(f"\n   Response snippet:\n{response.text[:1000]}")
                    
        except requests.Timeout:
            print("   ❌ Timeout - 서버 연결 시간 초과")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # If we found data, no need to try other keys
        if response.status_code == 200 and '<item>' in response.text:
            print(f"\n✓ API Key #{key_idx + 1} is working!")
            break

    print("\n" + "=" * 80)
    print("Test complete!")

finally:
    sys.stdout = original_stdout
    output_file.close()
    print("Output saved to api_test_result.txt")
