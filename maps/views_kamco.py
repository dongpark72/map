def kamco_proxy(request):
    """한국자산관리공사 온비드 공매물건 조회 프록시"""
    import requests
    import urllib.parse
    import xml.etree.ElementTree as ET
    from django.http import JsonResponse
    import logging

    logger = logging.getLogger(__name__)
    
    sido = request.GET.get('sido', '')
    sgk = request.GET.get('sgk', '')
    page = request.GET.get('page', 1)
    
    url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
    
    KEYS = [
        'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368',
        'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='
    ]
    
    def normalize_name(name):
        if not name: return ""
        mapping = {
            '서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시',
            '인천': '인천광역시', '광주': '광주광역시', '대전': '대전광역시',
            '울산': '울산광역시', '세종': '세종특별자치시', '경기': '경기도',
            '강원': '강원특별자치도', '충북': '충청북도', '충남': '충청남도',
            '전북': '전북특별자치도', '전남': '전라남도', '경북': '경상북도',
            '경남': '경상남도', '제주': '제주특별자치도'
        }
        return mapping.get(name, name)

    sido_norm = normalize_name(sido)
    
    def fetch_data(key, target_sido, target_sgk):
        try:
            raw_key = urllib.parse.unquote(key)
            query_params = [
                f"serviceKey={raw_key}",
                f"numOfRows=500",
                f"pageNo={page}",
                f"DPSL_MTD_CD=0001",
                f"SIDO={urllib.parse.quote(target_sido)}",
            ]
            if target_sgk:
                query_params.append(f"SGK={urllib.parse.quote(target_sgk)}")
            
            full_url = f"{url}?{'&'.join(query_params)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/xml,text/xml,*/*',
            }
            response = requests.get(full_url, headers=headers, timeout=15, verify=False)
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                header = root.find('header')
                result_code = header.find('resultCode').text if header is not None else ''
                if result_code == '00':
                    items = []
                    body = root.find('body')
                    if body is not None:
                        items_node = body.find('items')
                        if items_node is not None:
                            for item in items_node.findall('item'):
                                def get_v(tag):
                                    el = item.find(tag)
                                    return el.text.strip() if el is not None and el.text else ''
                                items.append({
                                    'CLTR_NM': get_v('CLTR_NM'),
                                    'LDNM_ADRS': get_v('LDNM_ADRS'),
                                    'NMRD_ADRS': get_v('NMRD_ADRS'),
                                    'APSL_ASES_AVG_AMT': get_v('APSL_ASES_AVG_AMT'),
                                    'FEE_RATE': get_v('FEE_RATE'),
                                    'USCBD_CNT': get_v('USCBD_CNT'),
                                    'GOODS_NM': get_v('GOODS_NM')
                                })
                    return items
            return None
        except Exception as e:
            logger.error(f"Kamco Fetch Error: {e}")
            return None

    for api_key in KEYS:
        results = fetch_data(api_key, sido_norm, sgk)
        if results is not None:
            if len(results) > 0 or not sgk:
                return JsonResponse({'status': 'OK', 'items': results})
            
            results_sido = fetch_data(api_key, sido_norm, "")
            if results_sido is not None:
                return JsonResponse({'status': 'OK', 'items': results_sido})

    return JsonResponse({'status': 'OK', 'items': []})
