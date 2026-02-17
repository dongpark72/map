
import os

views_path = 'maps/views.py'
kamco_code = """

def kamco_proxy(request):
    \"\"\"한국자산관리공사 온비드 공매물건 조회 프록시\"\"\"
    import requests
    import urllib.parse
    import xml.etree.ElementTree as ET
    
    sido = request.GET.get('sido', '')
    sgk = request.GET.get('sgk', '')
    emd = request.GET.get('emd', '')
    page = request.GET.get('page', 1)
    
    # API Keys from settings/env (reusing existing list logic structure if possible, but for safety defined here or reuse global)
    # Re-importing settings here to be safe inside function or assuming global context if file allows.
    # In views.py PUBLIC_DATA_KEYS is global.
    
    url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
    
    # Try keys
    # Assuming PUBLIC_DATA_KEYS is available in the module scope
    # If not, we define fallbacks
    KEYS = [
        'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==',
        'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    ]
    
    for api_key in KEYS:
        try:
            enc_key = urllib.parse.quote(api_key)
            
            # Construct Query String manually
            query_params = [
                f"serviceKey={enc_key}",
                f"pageNo={page}",
                f"numOfRows=100", 
                f"SIDO={urllib.parse.quote(sido)}",
                f"SGK={urllib.parse.quote(sgk)}"
            ]
            if emd:
                query_params.append(f"EMD={urllib.parse.quote(emd)}")
                
            full_url = f"{url}?{'&'.join(query_params)}"
            
            logger.info(f"Kamco Proxy Request: {sido} {sgk} {emd}")
            
            response = requests.get(full_url, timeout=10)
            
            if response.status_code == 200:
                if '<response>' in response.text:
                    try:
                        root = ET.fromstring(response.text)
                        header = root.find('header')
                        result_code = header.find('resultCode').text if header is not None else ''
                        
                        if result_code == '00':
                            items = []
                            body = root.find('body')
                            if body:
                                items_node = body.find('items')
                                if items_node:
                                    for item in items_node.findall('item'):
                                        def get_v(tag):
                                            el = item.find(tag)
                                            return el.text.strip() if el is not None and el.text else ''
                                        
                                        data = {
                                            'CLTR_NM': get_v('CLTR_NM'),
                                            'LDNM_ADRS': get_v('LDNM_ADRS'),
                                            'NMRD_ADRS': get_v('NMRD_ADRS'),
                                            'APSL_ASES_AVG_AMT': get_v('APSL_ASES_AVG_AMT'),
                                            'MIN_BID_PRC': get_v('MIN_BID_PRC'),
                                            'FEE_RATE': get_v('FEE_RATE'),
                                            'USCBD_CNT': get_v('USCBD_CNT'),
                                            'GOODS_NM': get_v('GOODS_NM'),
                                            'CTGR_FULL_NM': get_v('CTGR_FULL_NM'),
                                            'PBCT_BEGN_DTM': get_v('PBCT_BEGN_DTM'),
                                            'PBCT_CLS_DTM': get_v('PBCT_CLS_DTM'),
                                            'PBCT_CLTR_STAT_NM': get_v('PBCT_CLTR_STAT_NM'),
                                        }
                                        items.append(data)
                            
                            return JsonResponse({'status': 'OK', 'items': items})
                        else:
                            msg = header.find('resultMsg').text if header else 'Unknown Error'
                            if result_code == '30': continue
                            return JsonResponse({'status': 'ERROR', 'message': msg})
                            
                    except ET.ParseError:
                        continue
                else:
                     continue
            
        except Exception as e:
            logger.error(f"Kamco Proxy Error: {e}")
            continue

    return JsonResponse({'status': 'ERROR', 'message': 'Failed to fetch auction data'})
"""

try:
    # Read original file using 'rb' to avoid decoding errors
    with open(views_path, 'rb') as f:
        content = f.read()
    
    # Try to decode as utf-8 to find the split point
    # We look for the end of warehouse_proxy
    marker = b"return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)"
    
    idx = content.rfind(marker)
    if idx != -1:
        # Keep everything up to the marker + marker length
        new_content = content[:idx + len(marker)]
        
        # Add new content
        final_content = new_content.decode('utf-8') + "\n" + kamco_code
        
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print("Successfully repaired maps/views.py with Kamco proxy code.")
    else:
        print("Could not find the marker in views.py. File might be too corrupted.")
        
except Exception as e:
    print(f"Error repairing file: {e}")
