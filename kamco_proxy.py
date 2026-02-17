def kamco_proxy(request):
    """한국자산관리공사 온비드 공매물건 조회 프록시"""
    import requests
    import urllib.parse
    import xml.etree.ElementTree as ET
    
    sido = request.GET.get('sido', '')
    sgk = request.GET.get('sgk', '')
    emd = request.GET.get('emd', '')
    page = request.GET.get('page', 1)
    
    url = "http://apis.data.go.kr/B551142/ThingInfoInquireSvc/getUnifyUsageCltr"
    
    # Try keys
    for api_key in PUBLIC_DATA_KEYS:
        try:
            enc_key = urllib.parse.quote(api_key)
            params = {
                "serviceKey": api_key, # requests will encode this, but usually data.go.kr needs pre-encoded key if passed in query string manually, but with params dict requests handles it. Wait.
                # data.go.kr often has double encoding issues. 
                # In real_price_proxy they used `url = f"...serviceKey={enc_key}..."`.
                # I should follow that pattern to be safe.
            }
            
            # Construct Query String manually to ensure key is handled correctly
            query_params = [
                f"serviceKey={enc_key}",
                f"pageNo={page}",
                f"numOfRows=100", # Get enough items
                f"SIDO={urllib.parse.quote(sido)}",
                f"SGK={urllib.parse.quote(sgk)}"
            ]
            if emd:
                query_params.append(f"EMD={urllib.parse.quote(emd)}")
                
            full_url = f"{url}?{'&'.join(query_params)}"
            
            logger.info(f"Kamco Proxy Request: {sido} {sgk} {emd}")
            
            response = requests.get(full_url, timeout=10)
            
            if response.status_code == 200:
                # Check if valid XML response
                if '<response>' in response.text:
                    # Convert XML to JSON for frontend
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
                                        # Extract fields
                                        def get_v(tag):
                                            el = item.find(tag)
                                            return el.text.strip() if el is not None and el.text else ''
                                        
                                        data = {
                                            'CLTR_NM': get_v('CLTR_NM'), # 물건명
                                            'LDNM_ADRS': get_v('LDNM_ADRS'), # 소재지(지번)
                                            'NMRD_ADRS': get_v('NMRD_ADRS'), # 소재지(도로명)
                                            'APSL_ASES_AVG_AMT': get_v('APSL_ASES_AVG_AMT'), # 감정가
                                            'MIN_BID_PRC': get_v('MIN_BID_PRC'), # 최저입찰가
                                            'FEE_RATE': get_v('FEE_RATE'), # 최저입찰가율
                                            'USCBD_CNT': get_v('USCBD_CNT'), # 유찰횟수
                                            'GOODS_NM': get_v('GOODS_NM'), # 물건상세
                                            'CTGR_FULL_NM': get_v('CTGR_FULL_NM'), # 용도
                                            'PBCT_BEGN_DTM': get_v('PBCT_BEGN_DTM'),
                                            'PBCT_CLS_DTM': get_v('PBCT_CLS_DTM'),
                                            'PBCT_CLTR_STAT_NM': get_v('PBCT_CLTR_STAT_NM'), # 상태
                                        }
                                        items.append(data)
                            
                            return JsonResponse({'status': 'OK', 'items': items})
                        else:
                            msg = header.find('resultMsg').text if header else 'Unknown Error'
                            logger.error(f"Kamco API Logic Error: {msg}")
                            # Try next key if error is related to auth (though usually code 30 is auth)
                            if result_code == '30': continue
                            return JsonResponse({'status': 'ERROR', 'message': msg})
                            
                    except ET.ParseError:
                        logger.error("XML Parse Error in Kamco Proxy")
                        continue
                else:
                    # Not XML, maybe JSON or Error
                     continue
            
        except Exception as e:
            logger.error(f"Kamco Proxy Error with key: {e}")
            continue

    return JsonResponse({'status': 'ERROR', 'message': 'Failed to fetch auction data'})
