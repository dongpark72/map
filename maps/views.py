from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import ParcelCache, LandInfoCache, KamcoCache, WFSCache, WarehouseCache, HospitalCache
from .utils import validate_pnu, parse_pnu, get_pnu_alternatives, sort_buildings, format_date, normalize_bjdong_name
import requests
import json
import logging
import urllib.parse
import os
from datetime import datetime, timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)

# API Keys - 환경 변수 우선, 없으면 settings에서 가져옴
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', getattr(settings, 'GOOGLE_MAPS_API_KEY', ''))
PUBLIC_DATA_KEYS = [
    os.getenv('PUBLIC_DATA_KEY_1', 'eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=='),
    os.getenv('PUBLIC_DATA_KEY_2', 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'),
]
VWORLD_NED_KEY = os.getenv('VWORLD_NED_KEY', '98A53FD9-F542-32C4-9589-78A54E531AF7')

# API Timeouts
API_TIMEOUT_SHORT = 5
API_TIMEOUT_MEDIUM = 7
API_TIMEOUT_LONG = 10

def index(request):
    context = {
        'google_maps_api_key': GOOGLE_MAPS_API_KEY,
        'kakao_maps_api_key': settings.KAKAO_MAPS_API_KEY,
        'vworld_api_key': settings.VWORLD_API_KEY,
        'vworld_domain': 'http://map.goal-runner.com/',
    }
    return render(request, 'maps/index.html', context)

def portal(request):
    context = {
        'google_maps_api_key': GOOGLE_MAPS_API_KEY,
        'kakao_maps_api_key': settings.KAKAO_MAPS_API_KEY,
        'vworld_api_key': settings.VWORLD_API_KEY,
        'vworld_domain': 'http://map.goal-runner.com/',
    }
    return render(request, 'maps/map_app.html', context)

def parcel_proxy(request):
    pnu = request.GET.get('pnu')
    if not pnu:
        return JsonResponse({'error': 'PNU is required'}, status=400)
    
    # 1. 로컬 DB 캐시 확인
    try:
        cached = ParcelCache.objects.filter(pnu=pnu).first()
        if cached:
            return JsonResponse({
                'response': {
                    'status': 'OK',
                    'result': {
                        'featureCollection': {
                            'features': [{'geometry': cached.geometry_data}]
                        }
                    }
                },
                'source': 'local_cache'
            })
    except Exception as e:
        logger.error(f"Cache check failed: {e}")

    # 2. V-World 호출
    api_key = getattr(settings, 'VWORLD_API_KEY', None)
    if not api_key:
        return JsonResponse({
            'response': {'status': 'ERROR', 'error': {'message': 'V-World API Key가 설정되지 않았습니다.'}}
        })

    domain = 'http://map.goal-runner.com/'
    
    url = "https://api.vworld.kr/req/data"
    params = {
        "service": "data",
        "request": "GetFeature",
        "data": "LP_PA_CBND_BUBUN",
        "key": api_key,
        "domain": domain,
        "attrFilter": f"pnu:like:{pnu}",
        "format": "json",
        "geometry": "true"
    }
    
    try:
        logger.info(f"V-World Request: PNU={pnu}")
        response = requests.get(url, params=params, timeout=10)
        
        try:
            data = response.json()
        except Exception as json_e:
            logger.error(f"Failed to parse V-World JSON: {response.text}")
            return JsonResponse({
                'response': {'status': 'ERROR', 'error': {'message': 'V-World 응답이 올바른 JSON 형식이 아닙니다.'}}
            })

        # 3. 데이터 저장
        if data.get('response', {}).get('status') == 'OK':
            try:
                features = data['response'].get('result', {}).get('featureCollection', {}).get('features', [])
                if features:
                    ParcelCache.objects.update_or_create(
                        pnu=pnu,
                        defaults={'geometry_data': features[0]['geometry']}
                    )
            except Exception as inner_e:
                logger.error(f"Cache save failed: {inner_e}")
        
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Parcel Proxy Exception: {e}")
        return JsonResponse({
            'response': {'status': 'ERROR', 'error': {'message': f'시스템 오류: {str(e)}'}}
        }, status=200)



import concurrent.futures

def land_info_proxy(request):
    """토지이음에서 토지이용계획 정보를 가져오는 프록시 (병렬 처리 및 캐싱 적용)"""
    import xml.etree.ElementTree as ET
    from django.utils import timezone
    from datetime import timedelta
    
    pnu = request.GET.get('pnu')
    
    # PNU 검증
    if not validate_pnu(pnu):
        return JsonResponse({
            'status': 'ERROR',
            'message': 'Invalid PNU format. PNU must be 19 digits.'
        }, status=400)
    
    # 캐시 확인 (24시간 유효)
    try:
        cache = LandInfoCache.objects.filter(pnu=pnu).first()
        if cache and (timezone.now() - cache.updated_at) < timedelta(hours=24):
            logger.info(f"Cache hit for PNU: {pnu}")
            return JsonResponse({
                'status': 'OK',
                'pnu': pnu,
                'data': cache.data,
                'source': 'cache'
            })
    except Exception as e:
        logger.error(f"Cache check failed: {e}")

    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.eum.go.kr/web/am/amMain.jsp'
        }
        session.headers.update(headers)

        structured_data = {
            'land': {
                '소재지': '', '용도지역1': '', '용도지역2': '',
                '지목': '', '이용상황': '', '면적': '',
                '도로': '', '형상': '', '지세': '',
                '2026': '', '2025': '', '2024': '', '2023': '', '2022': '', '2021': '', '2020': ''
            },
            'buildings': []
        }

        # PNU 보정 로직 (유틸리티 함수 사용)
        pnus_to_try = get_pnu_alternatives(pnu)

        # 1. 토지 정보 API (V-World NED - 토지특성)
        def fetch_ned_data():
            try:
                connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
                ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
                
                for target_pnu in pnus_to_try:
                    # 100건을 가져와서 과거 공시지가까지 확보
                    query = f"{ned_url}^key={VWORLD_NED_KEY}|pnu={target_pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=100"
                    res = session.get(connector_url, params={'url': query}, timeout=API_TIMEOUT_MEDIUM)
                    if res.status_code == 200 and '<response>' in res.text:
                        root = ET.fromstring(res.text)
                        fields = root.findall('.//field')
                        if fields:
                            # 최신 데이터로 기본 정보 채우기
                            fields.sort(key=lambda x: x.find('stdrYear').text if x.find('stdrYear') is not None and x.find('stdrYear').text else '0', reverse=True)
                            latest = fields[0]
                            def get_v(e, t):
                                n = e.find(t); return n.text.strip() if n is not None and n.text else ''
                            
                            if not structured_data['land']['소재지']:
                                a = get_v(latest, 'ldCodeNm'); b = get_v(latest, 'mnnmSlno')
                                if a: structured_data['land']['소재지'] = f"{a} {b}"
                            
                            if not structured_data['land']['지목']: structured_data['land']['지목'] = get_v(latest, 'lndcgrCodeNm')
                            if not structured_data['land']['면적']: structured_data['land']['면적'] = get_v(latest, 'lndpclAr')
                            if not structured_data['land']['이용상황']: structured_data['land']['이용상황'] = get_v(latest, 'ladUseSittnNm')
                            if not structured_data['land']['도로']: structured_data['land']['도로'] = get_v(latest, 'roadSideCodeNm')
                            if not structured_data['land']['형상']: structured_data['land']['형상'] = get_v(latest, 'tpgrphFrmCodeNm')
                            if not structured_data['land']['지세']: structured_data['land']['지세'] = get_v(latest, 'tpgrphHgCodeNm')
                            
                            z1_v = get_v(latest, 'prposArea1Nm')
                            z2_v = get_v(latest, 'prposArea2Nm')
                            
                            if not structured_data['land']['용도지역1']:
                                structured_data['land']['용도지역1'] = z1_v
                                if not structured_data['land']['용도지역2'] and z2_v and z2_v != z1_v:
                                    structured_data['land']['용도지역2'] = z2_v
                            elif not structured_data['land']['용도지역2']:
                                if z1_v and z1_v != structured_data['land']['용도지역1']:
                                    structured_data['land']['용도지역2'] = z1_v
                                elif z2_v and z2_v != structured_data['land']['용도지역1']:
                                    structured_data['land']['용도지역2'] = z2_v
                            
                            # 과거 공시지가 채우기
                            for field in fields:
                                y = get_v(field, 'stdrYear'); p = get_v(field, 'pblntfPclnd')
                                target_years = ['2026', '2025', '2024', '2023', '2022', '2021', '2020']
                                if y in target_years and p:
                                    if not structured_data['land'].get(y):
                                        try:
                                            price_int = int(float(p))
                                            structured_data['land'][y] = "{:,}".format(price_int)
                                        except: 
                                            pass
                            break # 첫 번째 성공한 PNU에서 멈춤
            except requests.Timeout:
                logger.error(f"NED API Timeout for PNU: {pnu}")
            except ET.ParseError as e:
                logger.error(f"NED API XML Parse Error: {e}")
            except Exception as e:
                logger.error(f"NED API Error: {e}")

        # 2. 건축물 정보 API (국토교통부 건축물대장)
        def fetch_building_info():
            try:
                api_buildings = []
                connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
                api_url_recap = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
                api_url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
                api_url_flr = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
                
                found_api = False
                recap_found = False
                
                for target_pnu in pnus_to_try:
                    if found_api and recap_found: 
                        break
                    
                    # PNU 파싱 (유틸리티 함수 사용)
                    try:
                        params = parse_pnu(target_pnu)
                    except ValueError as e:
                        logger.error(f"PNU parsing error: {e}")
                        continue
                    
                    for api_key in PUBLIC_DATA_KEYS:
                        enc_key = urllib.parse.quote(api_key)
                        
                        # 1-1. 총괄표제부 (Recap)
                        if not recap_found:
                            try:
                                q_recap = f"{api_url_recap}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={params['sigunguCd']}|bjdongCd={params['bjdongCd']}|platGbCd={params['platGbCd']}|bun={params['bun']}|ji={params['ji']}"
                                res_recap = session.get(connector_url, params={'url': q_recap}, timeout=API_TIMEOUT_SHORT)
                                if res_recap.status_code == 200:
                                    items_recap = ET.fromstring(res_recap.text).findall('.//item')
                                    if items_recap:
                                        for item in items_recap:
                                            def get_t(tag):
                                                el = item.find(tag); return el.text.strip() if el is not None and el.text else ''
                                            b_data = {
                                                '건물명': get_t('bldNm'), '동명칭': '총괄표제부', 
                                                '주건물수': get_t('mainBldCnt'), '부속건물수': get_t('atchBldCnt'),
                                                '사용승인일': get_t('useAprDay'), '구조': get_t('strctCdNm'), 
                                                '지붕': get_t('roofCdNm'), '주용도': get_t('mainPurpsCdNm'),
                                                '지하': get_t('ugrndFlrCnt'), '지상': get_t('grndFlrCnt'), 
                                                '연면적': get_t('totArea'), '용적연면적': get_t('vlRatEstmTotArea'), 
                                                '건축면적': get_t('archArea'), '대지': get_t('platArea'),
                                                '높이': get_t('heit'), '건폐율': get_t('bcRat'), '용적률': get_t('vlRat')
                                            }
                                            api_buildings.insert(0, b_data)
                                        recap_found = True
                            except requests.Timeout:
                                logger.warning(f"Recap API timeout for key: {api_key[:20]}...")
                            except ET.ParseError as e:
                                logger.error(f"Recap API XML parse error: {e}")
                            except Exception as e:
                                logger.error(f"Recap API error: {e}")

                        # 1-2. 일반표제부 (Title)
                        if not found_api:
                            try:
                                q_title = f"{api_url_title}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={params['sigunguCd']}|bjdongCd={params['bjdongCd']}|platGbCd={params['platGbCd']}|bun={params['bun']}|ji={params['ji']}"
                                res_title = session.get(connector_url, params={'url': q_title}, timeout=API_TIMEOUT_MEDIUM)
                                if res_title.status_code == 200:
                                    root_title = ET.fromstring(res_title.text)
                                    items_title = root_title.findall('.//item')
                                    if items_title:
                                        for item in items_title:
                                            def get_t(tag):
                                                el = item.find(tag); return el.text.strip() if el is not None and el.text else ''
                                            b_data = {
                                                '건물명': get_t('bldNm'), '동명칭': get_t('dongNm'), 
                                                '사용승인일': get_t('useAprDay'), '구조': get_t('strctCdNm'), 
                                                '지붕': get_t('roofCdNm'), '주용도': get_t('mainPurpsCdNm'),
                                                '지하': get_t('ugrndFlrCnt'), '지상': get_t('grndFlrCnt'), 
                                                '연면적': get_t('totArea'), '용적연면적': get_t('vlRatEstmTotArea'), 
                                                '건축면적': get_t('archArea'), '대지': get_t('platArea'),
                                                '높이': get_t('heit'), '건폐율': get_t('bcRat'), '용적률': get_t('vlRat')
                                            }
                                            api_buildings.append(b_data)
                                        found_api = True
                            except requests.Timeout:
                                logger.warning(f"Title API timeout for key: {api_key[:20]}...")
                            except ET.ParseError as e:
                                logger.error(f"Title API XML parse error: {e}")
                            except Exception as e:
                                logger.error(f"Title API error: {e}")
                
                # 1-3. 층별 개요 API (누락된 동 명칭 보충)
                try:
                    found_dongs = {b.get('동명칭').strip() for b in api_buildings if b.get('동명칭')}
                    for target_pnu in pnus_to_try:
                        try:
                            params = parse_pnu(target_pnu)
                        except ValueError:
                            continue
                            
                        for api_key in PUBLIC_DATA_KEYS:
                            enc_key = urllib.parse.quote(api_key)
                            try:
                                q_flr = f"{api_url_flr}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={params['sigunguCd']}|bjdongCd={params['bjdongCd']}|platGbCd={params['platGbCd']}|bun={params['bun']}|ji={params['ji']}"
                                res_flr = session.get(connector_url, params={'url': q_flr}, timeout=API_TIMEOUT_MEDIUM)
                                if res_flr.status_code == 200:
                                    items_flr = ET.fromstring(res_flr.text).findall('.//item')
                                    for item in items_flr:
                                        d_nm = item.find('dongNm')
                                        d_nm_txt = d_nm.text.strip() if d_nm is not None and d_nm.text else ''
                                        if d_nm_txt and d_nm_txt not in found_dongs and '총괄' not in d_nm_txt:
                                            api_buildings.append({
                                                '건물명': '', '동명칭': d_nm_txt, '주용도': '층별정보참조',
                                                '사용승인일': '-', '구조': '-', '지붕': '-',
                                                '지하': '-', '지상': '-', '연면적': '-', '용적연면적': '-',
                                                '건축면적': '-', '대지': '-', '높이': '-', '건폐율': '-', '용적률': '-'
                                            })
                                            found_dongs.add(d_nm_txt)
                            except Exception:
                                pass
                except Exception as e:
                    logger.error(f"Floor API error: {e}")

                # 건물 정렬 (유틸리티 함수 사용)
                structured_data['buildings'] = sort_buildings(api_buildings)
                
            except Exception as e:
                logger.error(f"Building API Error: {e}")

        # 병렬 실행 (웹크롤링 제거, 오직 API만 사용)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(fetch_ned_data),
                executor.submit(fetch_building_info)
            ]
            concurrent.futures.wait(futures)

        # 캐시 저장 (성공적으로 데이터를 가져온 경우)
        try:
            LandInfoCache.objects.update_or_create(
                pnu=pnu,
                defaults={'data': structured_data}
            )
            logger.info(f"Cache saved for PNU: {pnu}")
        except Exception as e:
            logger.error(f"Cache save failed: {e}")

        return JsonResponse({'status': 'OK', 'pnu': pnu, 'data': structured_data})
        
    except requests.Timeout:
        logger.error(f"Timeout fetching land info for PNU: {pnu}")
        return JsonResponse({
            'status': 'ERROR',
            'message': '토지이음 서버 응답 시간 초과'
        })
    except Exception as e:
        logger.error(f"Land Info Proxy Exception: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return JsonResponse({
            'status': 'ERROR',
            'message': f'시스템 오류: {str(e)}'
        })

def building_detail_proxy(request):
    """건축물대장 정보 프록시 (총괄표제부 + 표제부 목록)"""
    import xml.etree.ElementTree as ET
    pnu = request.GET.get('pnu')

    logger.info(f"[Building Detail] Request for PNU: {pnu}")
    
    # PNU 검증
    if not validate_pnu(pnu):
        return JsonResponse({
            'status': 'ERROR',
            'message': 'Invalid PNU format'
        }, status=400)
    
    # PNU 보정 (유틸리티 함수 사용)
    pnus_to_try = get_pnu_alternatives(pnu)

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # API Endpoints
    api_url_recap = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
    api_url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

    result_data = {
        'recap': {}, 
        'titles': []
    }

    try:
        working_key = PUBLIC_DATA_KEYS[0]
        recap_item = None
        title_items = []

        # 1. 정보 수집
        found_any = False
        found_recap = False
        found_title = False
        
        for target_pnu in pnus_to_try:
            if found_recap and found_title: 
                break

            # PNU 파싱 (유틸리티 함수 사용)
            try:
                params = parse_pnu(target_pnu)
            except ValueError as e:
                logger.error(f"PNU parsing error: {e}")
                continue

            for key in PUBLIC_DATA_KEYS:
                enc_key = urllib.parse.quote(key)
                
                # 1-1. 총괄표제부 (Recap) 조회
                # numOfRows=1, pageNo=1 (총괄은 보통 1개)
                if not found_recap:
                    try:
                        q_recap = f"{api_url_recap}^serviceKey={enc_key}|numOfRows=1|pageNo=1|sigunguCd={params['sigunguCd']}|bjdongCd={params['bjdongCd']}|platGbCd={params['platGbCd']}|bun={params['bun']}|ji={params['ji']}"
                        res_recap = session.get(connector_url, params={'url': q_recap}, timeout=API_TIMEOUT_SHORT)
                        if res_recap.status_code == 200 and "<item>" in res_recap.text:
                            root = ET.fromstring(res_recap.text)
                            items = root.findall('.//item')
                            if items:
                                recap_item = items[0] # 첫번째 항목 사용
                                found_recap = True
                                found_any = True
                    except requests.Timeout:
                        logger.warning(f"Recap API timeout for key: {key[:20]}...")
                    except ET.ParseError as e:
                        logger.error(f"Recap XML parse error: {e}")
                    except Exception as e:
                        logger.error(f"Recap Error: {e}")

                # 1-2. 일반표제부 (Title) 목록 조회
                if not found_title:
                    try:
                        q_title = f"{api_url_title}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={params['sigunguCd']}|bjdongCd={params['bjdongCd']}|platGbCd={params['platGbCd']}|bun={params['bun']}|ji={params['ji']}"
                        res_title = session.get(connector_url, params={'url': q_title}, timeout=API_TIMEOUT_MEDIUM)
                        if res_title.status_code == 200 and "<item>" in res_title.text:
                            items = ET.fromstring(res_title.text).findall('.//item')
                            if items:
                                title_items.extend(items)
                                found_title = True
                                if not found_any: 
                                    found_any = True # Recap이 없어도 Title이 있으면 성공으로 간주
                    except requests.Timeout:
                        logger.warning(f"Title API timeout for key: {key[:20]}...")
                    except ET.ParseError as e:
                        logger.error(f"Title XML parse error: {e}")
                    except Exception as e:
                        logger.error(f"Title Error: {e}")
                
                if found_recap and found_title:
                    working_key = key
                    break
        
        # 2. 데이터 매핑
        def get_t(it, tag):
            if it is None: return ''
            el = it.find(tag); return el.text.strip() if el is not None and el.text else ''
        
        # (1) Recap Data Mapping
        # Recap이 없으면 Title 중 하나(가장 큰 것)를 Recap처럼 사용하거나 비워둠
        # 사용자 요청: "총괄표제부 및 표제부 순서" -> 총괄표제부가 없으면 일반표제부라도 보여주는게 좋음
        if recap_item is None and title_items:
             # 임시로 가장 큰 건물을 총괄정보로 사용
             recap_item = max(title_items, key=lambda x: float(get_t(x, 'totArea')) if get_t(x, 'totArea').replace('.','').isdigit() else 0)

        if recap_item is not None:
            # 주차/승강기 등은 총괄표제부에 있는 필드 그대로 사용
            result_data['recap'] = {
                '대지위치': get_t(recap_item, 'platPlc'),
                '도로명주소': get_t(recap_item, 'newPlatPlc'),
                '건물명': get_t(recap_item, 'bldNm'),
                '관련지번': get_t(recap_item, 'relatJibun') or f"{get_t(recap_item, 'bun')}-{get_t(recap_item, 'ji')}",
                '대지면적': get_t(recap_item, 'platArea'),
                '연면적': get_t(recap_item, 'totArea'),
                '건축면적': get_t(recap_item, 'archArea'),
                '용적면적': get_t(recap_item, 'vlRatEstmTotArea'),
                '건폐율': get_t(recap_item, 'bcRat'),
                '용적률': get_t(recap_item, 'vlRat'),
                '주건물수': get_t(recap_item, 'mainBldCnt'),
                '부속건물수': get_t(recap_item, 'atchBldCnt'),
                '호가구세대': f"{get_t(recap_item, 'hoCnt') or 0}/{get_t(recap_item, 'fmlyCnt') or 0}/{get_t(recap_item, 'hhldCnt') or 0}",
                '주용도': get_t(recap_item, 'mainPurpsCdNm'),
                '자주식주차': str(int(get_t(recap_item, 'indrAutoUtCnt') or 0) + int(get_t(recap_item, 'oudrAutoUtCnt') or 0)),
                '기계식주차': str(int(get_t(recap_item, 'indrMechUtCnt') or 0) + int(get_t(recap_item, 'oudrMechUtCnt') or 0)),
                '허가일': format_date(get_t(recap_item, 'pmsDay')),
                '사용승인일': format_date(get_t(recap_item, 'useAprDay'))
            }
        
        # (2) Titles (Building List) Mapping
        mapped_titles = []
        for it in title_items:
            # 동 명칭이 없으면 '주건물' 등 표시
            dong_nm = get_t(it, 'dongNm') or get_t(it, 'bldNm') or '-'
            mapped_titles.append({
                '구분': '주' if get_t(it, 'mainAtchGbCd') == '0' else '부', # 0:주건물, 1:부속건물
                '명칭': dong_nm,
                '구조': get_t(it, 'strctCdNm'),
                '지붕': get_t(it, 'roofCdNm'),
                '층수': f"{get_t(it, 'ugrndFlrCnt')}/{get_t(it, 'grndFlrCnt')}",
                '용도': get_t(it, 'mainPurpsCdNm'),
                '면적': get_t(it, 'totArea'), # 연면적
                'PK': get_t(it, 'mgmBldrgstPk')
            })

        # 정렬: 유틸리티 함수 사용
        result_data['titles'] = sort_buildings(mapped_titles, '명칭')

        return JsonResponse({'status': 'OK', 'data': result_data})

    except Exception as e:
        logger.error(f"Building Detail Error: {e}")
        import traceback
        return JsonResponse({'status': 'ERROR', 'message': f"{str(e)}\n{traceback.format_exc()}"})


def floor_info_proxy(request):
    """층별 정보 조회 API"""
    import xml.etree.ElementTree as ET
    
    pnu = request.GET.get('pnu')
    mgm_bldrgst_pk = request.GET.get('pk')  # 관리건축물대장PK
    dong_nm = request.GET.get('dongNm', '')  # 동명칭 (선택)
    
    logger.info(f"[Floor Info] Request - PNU: {pnu}, PK: {mgm_bldrgst_pk}, DongNm: {dong_nm}")
    
    # PNU 검증
    if not validate_pnu(pnu):
        return JsonResponse({
            'status': 'ERROR',
            'message': 'Invalid PNU format'
        }, status=400)
    
    # PNU 보정
    pnus_to_try = get_pnu_alternatives(pnu)
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    api_url_flr = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrFlrOulnInfo"
    
    floor_items = []
    
    try:
        for target_pnu in pnus_to_try:
            if floor_items:
                break
            
            # PNU 파싱
            try:
                params = parse_pnu(target_pnu)
            except ValueError as e:
                logger.error(f"PNU parsing error: {e}")
                continue
            
            for api_key in PUBLIC_DATA_KEYS:
                enc_key = urllib.parse.quote(api_key)
                
                try:
                    q_flr = f"{api_url_flr}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={params['sigunguCd']}|bjdongCd={params['bjdongCd']}|platGbCd={params['platGbCd']}|bun={params['bun']}|ji={params['ji']}"
                    
                    # 동명칭이 있으면 추가 필터링을 위해 파라미터에 포함 (API가 지원하는 경우)
                    # 대부분의 경우 dongNm 파라미터를 지원하지 않으므로 응답 후 필터링
                    
                    res_flr = session.get(connector_url, params={'url': q_flr}, timeout=API_TIMEOUT_MEDIUM)
                    
                    if res_flr.status_code == 200 and "<item>" in res_flr.text:
                        root = ET.fromstring(res_flr.text)
                        items = root.findall('.//item')
                        
                        if items:
                            # 동명칭으로 필터링 (지정된 경우)
                            if dong_nm:
                                items = [item for item in items 
                                        if item.find('dongNm') is not None 
                                        and item.find('dongNm').text 
                                        and item.find('dongNm').text.strip() == dong_nm]
                            
                            floor_items = items
                            logger.info(f"[Floor Info] Found {len(floor_items)} floor items")
                            break
                            
                except requests.Timeout:
                    logger.warning(f"Floor API timeout for key: {api_key[:20]}...")
                except ET.ParseError as e:
                    logger.error(f"Floor XML parse error: {e}")
                except Exception as e:
                    logger.error(f"Floor API error: {e}")
        
        # 데이터 매핑
        def get_t(it, tag):
            if it is None: return ''
            el = it.find(tag)
            return el.text.strip() if el is not None and el.text else ''
        
        floors = []
        for item in floor_items:
            flr_gb_cd = get_t(item, 'flrGbCd')  # 10:지하, 20:지상, 30:옥탑...
            flr_no = get_t(item, 'flrNo')
            
            floor_data = {
                '구분': get_t(item, 'mainAtchGbCdNm') or '주',  # 주/부속
                '층별': get_t(item, 'flrNoNm') or f"{flr_no}층",  # 층번호명
                '구조': get_t(item, 'strctCdNm'),  # 구조
                '용도': get_t(item, 'mainPurpsCdNm'),  # 주용도
                '면적': get_t(item, 'area'),  # 면적
                '층구분': flr_gb_cd,
                '층번호': flr_no,
                '동명칭': get_t(item, 'dongNm')  # 동명칭
            }
            floors.append(floor_data)
        
        # 층별 정렬 로직 개선 (지하 -> 지상 -> 옥탑 순, 각 그룹 내 오름차순)
        def floor_sort_key(f):
            try:
                gb = f['층구분'] or '20' # 기본값 지상
                no = int(f['층번호'] or 0)
                
                # 정렬 가중치 계산
                # 지하(10): -100 + no (B2는 no=2이므로 -98, B1은 no=1이므로 -99... 가 아니라 B1이 -1, B2가 -2인 경우가 많음)
                # API 명세상 flrNo는 그냥 숫자임. B1은 1, B2는 2...
                # 그래서 지하의 경우 no를 음수로 처리하여 정렬
                if gb == '10': # 지하
                    return -1000 - no # B2(-1002) < B1(-1001)
                elif gb == '20': # 지상
                    return no # 1 < 2 < 3
                elif gb == '30': # 옥탑
                    return 1000 + no # 옥탑1 < 옥탑2
                else:
                    return no
            except:
                return 0
        
        floors.sort(key=floor_sort_key)
        
        return JsonResponse({
            'status': 'OK',
            'data': {
                'floors': floors,
                'count': len(floors),
                'dongNm': dong_nm
            }
        })
        
    except Exception as e:
        logger.error(f"Floor Info Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return JsonResponse({
            'status': 'ERROR',
            'message': f'시스템 오류: {str(e)}'
        })


def real_price_proxy(request):
    """실거래가 정보를 가져와서 반환하는 프록시 (최근 24개월)"""
    import xml.etree.ElementTree as ET
    from concurrent.futures import ThreadPoolExecutor
    
    sigungu_cd = request.GET.get('sigunguCd') # LAWD_CD (5자리)
    bjdong_cd = request.GET.get('bjdongCd')   # 법정동코드 (10자리 중 앞 5자리는 sigunguCd와 동일)
    bjdong_nm = request.GET.get('bjdongNm', '') # 비교용 법정동명 (ex: 미음동, 감전동)
    trade_type = request.GET.get('type', 'apt') # apt, row, offi, detached, land, biz, factory
    
    if not sigungu_cd:
        return JsonResponse({'status': 'ERROR', 'message': 'sigunguCd is required'}, status=400)

    # API 유형별 엔드포인트 매핑
    api_map = {
        'apt': 'http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade',
        'row': 'http://apis.data.go.kr/1613000/RTMSDataSvcRHTrade/getRTMSDataSvcRHTrade',
        'offi': 'http://apis.data.go.kr/1613000/RTMSDataSvcOffiTrade/getRTMSDataSvcOffiTrade',
        'detached': 'http://apis.data.go.kr/1613000/RTMSDataSvcSHTrade/getRTMSDataSvcSHTrade',
        'land': 'http://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade',
        'biz': 'http://apis.data.go.kr/1613000/RTMSDataSvcNrgTrade/getRTMSDataSvcNrgTrade',
        'factory': 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'
    }
    
    base_url = api_map.get(trade_type)
    if not base_url:
        return JsonResponse({'status': 'ERROR', 'message': f'Unknown trade type: {trade_type}'}, status=400)

    session = requests.Session()
    # 토지이음 커넥터 사용 (보안 및 접근성 확보)
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # 최근 24개월 리스트 생성 (YYYYMM)
    now = datetime.now()
    months = []
    for i in range(24):
        year = now.year
        month = now.month - i
        while month <= 0:
            month += 12
            year -= 1
        months.append(f"{year}{month:02d}")
    
    months = sorted(list(set(months)), reverse=True)
    all_items = []
    norm_target_bjdong = normalize_bjdong_name(bjdong_nm)

    def fetch_month_data(ym):
        temp_items = []
        for api_key in PUBLIC_DATA_KEYS:
            enc_key = urllib.parse.quote(api_key)
            try:
                # 파라미터 구성 (대부분 LAWD_CD, DEAL_YMD 사용)
                query = f"{base_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={ym}|numOfRows=999"
                
                res = session.get(connector_url, params={'url': query}, timeout=API_TIMEOUT_LONG)
                if res.status_code == 200 and '<item>' in res.text:
                    try:
                        root = ET.fromstring(res.text)
                    except ET.ParseError:
                        continue # XML 파싱 실패 시 다음 키 시도
                        
                    items = root.findall('.//item')
                    for item in items:
                        def get_v(tag):
                            el = item.find(tag)
                            return el.text.strip() if el is not None and el.text else ''
                        
                        # 법정동 비교 (lenient comparison)
                        # API마다 필드명이 '법정동' 또는 'umdNm' 임
                        item_umd = get_v('umdNm')
                        item_bjdong_raw = get_v('법정동') or item_umd or ''
                        
                        if bjdong_nm:
                            norm_item_bjdong = normalize_bjdong_name(item_bjdong_raw)
                            # '동'을 포함하거나 포함되는 경우 (ex: 미음동 vs 부산광역시 강서구 미음동)
                            if norm_target_bjdong not in norm_item_bjdong and norm_item_bjdong not in norm_target_bjdong:
                                continue
                        
                        # 아이템 데이터 구성
                        data = {
                            'dealYear': get_v('dealYear') or get_v('년'),
                            'dealMonth': get_v('dealMonth') or get_v('월'),
                            'dealDay': get_v('dealDay') or get_v('일'),
                            'dealAmount': get_v('dealAmount') or get_v('거래금액'),
                            'jibun': get_v('jibun') or get_v('지번'),
                            'umdNm': item_bjdong_raw,
                            'buildYear': get_v('buildYear') or get_v('건축년도'),
                        }
                        
                        # 유형별 특화 필드
                        if trade_type == 'factory':
                            data.update({
                                'buildingType': get_v('buildingType'), # 건물유형
                                'buildingUse': get_v('buildingUse'),   # 건물주용도
                                'landUse': get_v('landUse'),           # 용도지역
                                'floor': get_v('floor') or get_v('층'),
                                'plottageAr': get_v('plottageAr') or get_v('대지면적'),
                                'buildingAr': get_v('buildingAr') or get_v('건물면적'),
                            })
                        elif trade_type == 'apt':
                            data.update({
                                'name': get_v('aptNm') or get_v('apartment') or get_v('아파트'),
                                'area': get_v('excluUseAr') or get_v('전용면적'),
                                'floor': get_v('floor') or get_v('층'),
                            })
                        elif trade_type == 'offi':
                            data.update({
                                'name': get_v('offiNm') or get_v('오피스텔'),
                                'area': get_v('excluUseAr') or get_v('전용면적'),
                                'floor': get_v('floor') or get_v('층'),
                            })
                        elif trade_type == 'row':
                            data.update({
                                'name': get_v('mhouseNm') or get_v('연립다세대') or get_v('건물명'),
                                'excluUseAr': get_v('excluUseAr') or get_v('전용면적'),
                                'landAr': get_v('landAr') or get_v('대지권면적'),
                                'floor': get_v('floor') or get_v('층'),
                            })
                        elif trade_type == 'land':
                            data.update({
                                'area': get_v('dealArea') or get_v('area') or get_v('대지면적'),
                                'landUse': get_v('landUse') or get_v('용도지역'),
                                'lndcgrNm': get_v('jimok') or get_v('lndcgrNm') or get_v('지목'),
                            })
                        elif trade_type == 'biz':
                            data.update({
                                'name': get_v('건물명') or get_v('bldNm'),
                                'buildingUse': get_v('buildingUse') or get_v('건물주용도'),
                                'plottageAr': get_v('plottageAr') or get_v('대지면적'),
                                'buildingAr': get_v('buildingAr') or get_v('건물면적'),
                                'floor': get_v('floor') or get_v('층'),
                            })
                        elif trade_type == 'detached':
                            data.update({
                                'houseType': get_v('houseType') or get_v('주택유형'),
                                'totalFloorAr': get_v('totalFloorAr') or get_v('연면적'),
                                'plottageAr': get_v('plottageAr') or get_v('대지면적'),
                            })
                        
                        temp_items.append(data)
                    return temp_items # 한 달치 성공하면 반환 (다음 키 시도 안 함)
            except Exception as e:
                logger.error(f"Error fetching RealPrice for {ym} with key {api_key[:10]}: {e}")
        return []

    # 병렬 처리로 24개월 조회
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(fetch_month_data, months))
        for res_list in results:
            all_items.extend(res_list)

    # 계약일 순 정렬
    def sort_key(x):
        try:
            return (int(x['dealYear']), int(x['dealMonth']), int(x['dealDay']))
        except:
            return (0, 0, 0)
    
    all_items.sort(key=sort_key, reverse=True)

    return JsonResponse({
        'status': 'OK',
        'type': trade_type,
        'count': len(all_items),
        'data': all_items
    })

def wfs_proxy(request):
    """V-World WFS API Proxy with Server-side Caching"""
    from django.conf import settings
    import requests
    from django.http import HttpResponse, JsonResponse
    from .models import WFSCache
    from django.utils import timezone
    from datetime import timedelta
    import hashlib

    typename = request.GET.get('typename')
    bbox = request.GET.get('bbox')
    srsname = request.GET.get('srsname', 'EPSG:4326')
    
    if not typename or not bbox:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # 1. Round BBOX to 3 decimal places for better cache hits (~110m grid)
    try:
        coords = [float(x) for x in bbox.split(',')]
        rounded_bbox = ','.join([f"{round(x, 3):.3f}" for x in coords])
    except:
        rounded_bbox = bbox

    # 2. Check Cache
    cache_key = f"{typename}_{rounded_bbox}_{srsname}"
    # Use MD5 hash for key if it's too long, but here we can just use it
    try:
        cached = WFSCache.objects.filter(cache_key=cache_key).first()
        if cached and (timezone.now() - cached.created_at) < timedelta(hours=1):
            return HttpResponse(json.dumps(cached.data), content_type="application/json")
    except Exception as e:
        logger.error(f"WFS Cache check error: {e}")

    # 3. External Request
    url = "https://api.vworld.kr/req/wfs"
    params = {
        "key": settings.VWORLD_API_KEY,
        "domain": getattr(settings, 'VWORLD_DOMAIN', 'http://175.126.187.59:8000/'),
        "service": "WFS",
        "version": "1.1.0",
        "request": "GetFeature",
        "typename": typename,
        "bbox": bbox,
        "srsname": srsname,
        "output": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # 4. Simplify GeoJSON Data to improve performance
            data = simplify_geojson(data, typename)
            
            # Save to Cache
            try:
                WFSCache.objects.update_or_create(
                    cache_key=cache_key,
                    defaults={'data': data, 'created_at': timezone.now()}
                )
            except Exception as e:
                logger.error(f"WFS Cache save error: {e}")
            
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'V-World API error', 'status': response.status_code}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def simplify_geojson(data, typename):
    """Simplifies GeoJSON coordinates to reduce data size and improve rendering speed"""
    # Define tolerance in degrees (approx 111,000m per degree)
    # SIDO: ~20m, SIG: ~5m, EMD: ~1m, RI: ~0.5m
    tolerances = {
        'lt_c_adsido_info': 0.0002,
        'lt_c_adsigg_info': 0.00005,
        'lt_c_ademd_info': 0.00001,
        'lt_c_adri_info': 0.000005
    }
    tolerance = tolerances.get(typename, 0.000005)
    
    if 'features' not in data:
        return data
        
    for feature in data['features']:
        geom = feature.get('geometry')
        if not geom: continue
        
        g_type = geom.get('type')
        coords = geom.get('coordinates')
        if not coords: continue
        
        if g_type == 'Polygon':
            new_coords = []
            for ring in coords:
                new_coords.append(simplify_line(ring, tolerance))
            geom['coordinates'] = new_coords
        elif g_type == 'MultiPolygon':
            new_multi = []
            for poly in coords:
                new_poly = []
                for ring in poly:
                    new_poly.append(simplify_line(ring, tolerance))
                new_multi.append(new_poly)
            geom['coordinates'] = new_multi
            
    return data

def simplify_line(points, tolerance):
    """Douglas-Peucker algorithm implementation for point list simplification"""
    # points: [[lng, lat], [lng, lat], ...]
    if len(points) <= 2:
        return [[round(p[0], 6), round(p[1], 6)] for p in points]
    
    tol_sq = tolerance ** 2
    
    def get_distance_sq(p, p1, p2):
        x, y = p
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 and y1 == y2:
            return (x-x1)**2 + (y-y1)**2
        dx = x2 - x1
        dy = y2 - y1
        t = ((x-x1)*dx + (y-y1)*dy) / (dx*dx + dy*dy)
        t = max(0, min(1, t))
        cx = x1 + t*dx
        cy = y1 + t*dy
        return (x-cx)**2 + (y-cy)**2

    def dp(pts, sq_tol):
        n = len(pts)
        if n <= 2:
            return pts
        dmax_sq = 0
        idx = -1
        p1 = pts[0]
        p2 = pts[-1]
        for i in range(1, n-1):
            d_sq = get_distance_sq(pts[i], p1, p2)
            if d_sq > dmax_sq:
                dmax_sq = d_sq
                idx = i
        if dmax_sq > sq_tol:
            res1 = dp(pts[:idx+1], sq_tol)
            res2 = dp(pts[idx:], sq_tol)
            return res1[:-1] + res2
        else:
            return [pts[0], pts[-1]]

    simplified = dp(points, tol_sq)
    # Final rounding to 6 decimal places (~0.1m precision)
    return [[round(p[0], 6), round(p[1], 6)] for p in simplified]





def warehouse_proxy(request):
    """경기도 물류창고 API 프록시 (캐싱 적용)"""
    import requests
    from django.utils import timezone
    from datetime import timedelta

    sigun_nm = request.GET.get('sigun', '')
    p_index = request.GET.get('page', 1)
    p_size = request.GET.get('size', 1000)
    
    cache_key = f"warehouse_{sigun_nm}_{p_index}_{p_size}"
    
    try:
        cached = WarehouseCache.objects.filter(cache_key=cache_key).first()
        if cached and (timezone.now() - cached.created_at) < timedelta(hours=24):
            return JsonResponse(cached.data)
    except Exception as e:
        logger.error(f"Warehouse Cache Read Error: {e}")

    api_key = '11411d4d3b464c10a5fe57edb2917d17'
    url = "https://openapi.gg.go.kr/LogisticsWarehouse"
    
    params = {
        "KEY": api_key,
        "Type": "json",
        "pIndex": p_index,
        "pSize": p_size
    }
    
    if sigun_nm:
        params['SIGUN_NM'] = sigun_nm
        
    try:
        logger.info(f"Fetching Warehouse Data: sigun={sigun_nm}")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            try:
                WarehouseCache.objects.update_or_create(
                    cache_key=cache_key,
                    defaults={'data': data, 'created_at': timezone.now()}
                )
            except Exception as e:
                logger.error(f"Warehouse Cache Save Error: {e}")
            
            return JsonResponse(data)
        else:
            return JsonResponse({'status': 'ERROR', 'message': f'API Error: {response.status_code}'}, status=response.status_code)
            
    except Exception as e:
        logger.error(f"Warehouse API Error: {e}")
        return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)

def kamco_proxy(request):
    """한국자산관리공사 온비드 공매물건 조회 프록시 (데이터베이스 캐싱 적용)"""
    import requests
    import urllib.parse
    import xml.etree.ElementTree as ET
    from django.http import JsonResponse
    from django.utils import timezone
    from datetime import timedelta
    
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
    
    def get_cached_data(target_sido, target_sgk, target_page):
        cache_key = f"kamco_{target_sido}_{target_sgk}_{target_page}"
        try:
            cached = KamcoCache.objects.filter(cache_key=cache_key).first()
            if cached and (timezone.now() - cached.created_at) < timedelta(hours=6):
                return cached.data
        except Exception as e:
            logger.error(f"Kamco Cache Read Error: {e}")
        return None

    def save_cached_data(target_sido, target_sgk, target_page, data):
        cache_key = f"kamco_{target_sido}_{target_sgk}_{target_page}"
        try:
            KamcoCache.objects.update_or_create(
                cache_key=cache_key,
                defaults={'data': data, 'created_at': timezone.now()}
            )
        except Exception as e:
            logger.error(f"Kamco Cache Save Error: {e}")

    def fetch_data(key, target_sido, target_sgk, ctgr_id=None):
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
            if ctgr_id:
                query_params.append(f"CTGR_ID={ctgr_id}")
            
            full_url = f"{url}?{'&'.join(query_params)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/xml,text/xml,*/*',
            }
            response = requests.get(full_url, headers=headers, timeout=10, verify=False)
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
                                
                                # 기본 필드 값 가져오기
                                land_sqms = get_v('LAND_SQMS')
                                bld_sqms = get_v('BLD_SQMS')
                                bid_prgn_nft = get_v('BID_PRGN_NFT')
                                goods_nm = get_v('GOODS_NM')
                                ctgr_full_nm = get_v('CTGR_FULL_NM')
                                
                                # 부동산이 아닌 물건 필터링 (자동차, 유가증권, 기계 등 제외)
                                # CTGR_FULL_NM에 "토지", "건물", "대지", "임야", "전", "답", "주택" 등이 포함되어야 함
                                real_estate_keywords = ['토지', '건물', '대지', '임야', '전', '답', '주택', '아파트', '오피스텔', '상가', '공장']
                                exclude_keywords = ['자동차', '차량', '운송', '증권', '과리', '기계', '장비', '물품']
                                
                                is_real_estate = False
                                if ctgr_full_nm:
                                    # 제외 키워드가 있으면 스킵
                                    if any(keyword in ctgr_full_nm for keyword in exclude_keywords):
                                        continue
                                    # 부동산 키워드가 있으면 포함
                                    if any(keyword in ctgr_full_nm for keyword in real_estate_keywords):
                                        is_real_estate = True
                                
                                # 부동산이 아니면 스킵
                                if not is_real_estate:
                                    continue
                                
                                # GOODS_NM에서 백업 정보 파싱 (API 필드가 비어있을 때)
                                if not land_sqms and goods_nm:
                                    import re
                                    land_match = re.search(r'토지\s*([0-9,.]+)\s*㎡', goods_nm)
                                    if land_match:
                                        land_sqms = land_match.group(1)
                                
                                if not bld_sqms and goods_nm:
                                    import re
                                    bld_match = re.search(r'건물\s*([0-9,.]+)\s*㎡', goods_nm)
                                    if bld_match:
                                        bld_sqms = bld_match.group(1)
                                
                                # 입찰 회수: BID_PRGN_NFT가 비어있으면 BID_MNMT_NO 사용
                                if not bid_prgn_nft:
                                    bid_mnmt_no = get_v('BID_MNMT_NO')
                                    if bid_mnmt_no:
                                        # '0011' -> '11', '0014' -> '14' 형식으로 변환
                                        try:
                                            bid_prgn_nft = str(int(bid_mnmt_no))
                                        except:
                                            pass
                                
                                # GOODS_NM에서도 시도
                                if not bid_prgn_nft and goods_nm:
                                    import re
                                    bid_match = re.search(r'(\d+)회\s*입찰', goods_nm)
                                    if bid_match:
                                        bid_prgn_nft = bid_match.group(1)
                                
                                items.append({
                                    'CLTR_NM': get_v('CLTR_NM'),
                                    'PBCT_CLTR_STAT_NM': get_v('PBCT_CLTR_STAT_NM'),
                                    'LDNM_ADRS': get_v('LDNM_ADRS'),
                                    'NMRD_ADRS': get_v('NMRD_ADRS'),
                                    'CTGR_FULL_NM': get_v('CTGR_FULL_NM'),
                                    'LAND_SQMS': land_sqms,
                                    'BLD_SQMS': bld_sqms,
                                    'MIN_BID_PRC': get_v('MIN_BID_PRC'),
                                    'BID_PRGN_NFT': bid_prgn_nft,
                                    'GOODS_NM': goods_nm
                                })
                    return items
            return None
        except Exception as e:
            logger.error(f"Kamco Fetch Error: {e}")
            return None

    # 1. 시군구 검색 (캐시 확인)
    results = get_cached_data(sido_norm, sgk, page)
    if results is not None:
        if len(results) > 0 or not sgk:
            return JsonResponse({'status': 'OK', 'items': results, 'cached': True})

    # 2. 시군구 검색 (API 호출) - 부동산(토지/건물)만 필터링 (CTGR_ID=10000)
    for api_key in KEYS:
        results = fetch_data(api_key, sido_norm, sgk, '10000')  # 부동산 카테고리만
        
        if results:
            save_cached_data(sido_norm, sgk, page, results)
            return JsonResponse({'status': 'OK', 'items': results, 'cached': False, 'count': len(results)})
        elif results is not None:
            save_cached_data(sido_norm, sgk, page, [])
            break

    # 3. 시군구 결과가 없고 sgk가 있는 경우 시도 전체 검색
    if sgk:
        # 시도 캐시 확인
        results_sido = get_cached_data(sido_norm, "", page)
        if results_sido is not None:
            return JsonResponse({'status': 'OK', 'items': results_sido, 'cached': True, 'scope': 'sido'})
        
        # 시도 API 호출 - 부동산(토지/건물)만 필터링 (CTGR_ID=10000)
        for api_key in KEYS:
            results_sido = fetch_data(api_key, sido_norm, "", '10000')  # 부동산 카테고리만
            
            if results_sido:
                save_cached_data(sido_norm, "", page, results_sido)
                return JsonResponse({'status': 'OK', 'items': results_sido, 'cached': False, 'scope': 'sido', 'count': len(results_sido)})
            elif results_sido is not None:
                save_cached_data(sido_norm, "", page, [])
                break

    return JsonResponse({'status': 'OK', 'items': []})

def hospital_proxy(request):
    """보건복지부 병의원 병상수 API 프록시 (캐싱 적용)"""
    import requests
    from django.utils import timezone
    from datetime import timedelta
    import xml.etree.ElementTree as ET

    year = request.GET.get('year', '')
    dvsd = request.GET.get('dvsd', '') # 시도구분
    
    # 캐시 키 생성 (year와 dvsd 기반)
    cache_key = f"hospital_{year}_{dvsd}"
    
    try:
        cached = HospitalCache.objects.filter(cache_key=cache_key).first()
        if cached and (timezone.now() - cached.created_at) < timedelta(hours=24):
            return JsonResponse(cached.data)
    except Exception as e:
        logger.error(f"Hospital Cache Read Error: {e}")

    url = "http://apis.data.go.kr/1352000/ODMS_STAT_15/callStat15Api"
    
    # PUBLIC_DATA_KEYS 중 하나 사용 (동작이 확인된 두 번째 키 우선 사용 권장)
    api_key = PUBLIC_DATA_KEYS[1] if len(PUBLIC_DATA_KEYS) > 1 else PUBLIC_DATA_KEYS[0]
    
    params = {
        "serviceKey": api_key,
        "apiType": "JSON",
        "numOfRows": 100,
        "pageNo": 1
    }
    
    if not year:
        year = "2023" # 데이터 확인된 최신 년도 기본값
    params['year'] = year
    
    if dvsd:
        params['dvsd'] = dvsd
        
    try:
        logger.info(f"Fetching Hospital Data: year={year}, dvsd={dvsd}")
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # 캐시 저장
                HospitalCache.objects.update_or_create(
                    cache_key=cache_key,
                    defaults={'data': data, 'created_at': timezone.now()}
                )
                
                return JsonResponse(data)
            except Exception as json_e:
                logger.error(f"Hospital API JSON Parse Error: {json_e}, Response: {response.text[:200]}")
                return JsonResponse({'status': 'ERROR', 'message': 'Invalid JSON response from API'}, status=500)
        else:
            return JsonResponse({'status': 'ERROR', 'message': f'API Error: {response.status_code}'}, status=response.status_code)
            
    except Exception as e:
        logger.error(f"Hospital API Error: {e}")
        return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hospital_detail_proxy(request):
    """건강보험심사평가원(HIRA) 개별 병원 상세 정보(병상수 등) 프록시 (Direct Call 사용)"""
    import requests
    import urllib.parse
    from django.utils import timezone
    from datetime import timedelta
    
    hospital_name = request.GET.get('name', '')
    ykiho = request.GET.get('ykiho', '')

    # Cache key: prefer ykiho if available
    cache_key = f"hosp_detail_{ykiho}" if ykiho else f"hosp_detail_{hospital_name}"
    
    if not hospital_name and not ykiho:
        return JsonResponse({'status': 'ERROR', 'message': 'Hospital name or ykiho is required'}, status=400)
    
    # 캐시 확인
    try:
        cached = HospitalCache.objects.filter(cache_key=cache_key).first()
        if cached and (timezone.now() - cached.created_at) < timedelta(hours=24):
            return JsonResponse(cached.data)
    except Exception as e:
        logger.error(f"Hospital Detail Cache Read Error: {e}")

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    # 올바른 키 사용 (Hex Key) - 사용자 제공 키로 고정
    api_key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    
    basis_info = {}
    
    # ykiho가 없으면 이름으로 검색 (기존 로직)
    if not ykiho:
        # 1단계: 병원 이름으로 요양기호(ykiho) 조회
        basis_url = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
        # ... params ...
        params_basis = {
            'serviceKey': api_key,
            'pageNo': '1',
            'numOfRows': '1',
            '_type': 'json',
            'yadmNm': hospital_name
        }
        
        try:
             basis_res = requests.get(basis_url, params=params_basis, timeout=10)
             if basis_res.status_code == 200:
                 basis_data = basis_res.json()
                 # Safe extraction
                 items = []
                 response_obj = basis_data.get('response')
                 if isinstance(response_obj, dict):
                     body = response_obj.get('body')
                     if isinstance(body, dict):
                         items_wrapper = body.get('items')
                         if isinstance(items_wrapper, dict):
                             extracted_items = items_wrapper.get('item')
                             if extracted_items:
                                 items = extracted_items
                 
                 if items:
                     if isinstance(items, list):
                         ykiho = items[0].get('ykiho')
                         basis_info = items[0]
                     else:
                         ykiho = items.get('ykiho')
                         basis_info = items
        except Exception as e:
             logger.error(f"Basis Search Error: {e}")
    
    if not ykiho:
         return JsonResponse({'status': 'ERROR', 'message': 'ykiho not found for name'}, status=404)

    try:

        # 2단계: 요양기호로 시설정보(병상수 등) 조회
        # URL: https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7
        detail_url = "https://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getEqpInfo2.7"
        
        logger.info(f"Fetching HIRA Detail Info for ykiho: {ykiho} (Direct)")
        params_detail = {
            'serviceKey': api_key,
            'pageNo': '1',
            'numOfRows': '1',
            '_type': 'json',
            'ykiho': ykiho
        }
        
        # HTTPS verify=False 추가 (서버 환경 고려)
        detail_res = requests.get(detail_url, params=params_detail, verify=False, timeout=10)
        
        if detail_res.status_code == 200:
            try:
                detail_data = detail_res.json()
                
                # Safely navigate: response -> body -> items
                response_obj = detail_data.get('response')
                if isinstance(response_obj, dict):
                    body = response_obj.get('body')
                    if isinstance(body, dict):
                        items_wrapper = body.get('items')
                        if isinstance(items_wrapper, dict):
                            detail_items = items_wrapper.get('item', {})
                            if isinstance(detail_items, list) and len(detail_items) > 0:
                                detail_items = detail_items[0]
                        else:
                            detail_items = {}
                    else:
                        detail_items = {}
                else:
                    detail_items = {}
            except Exception as e:
                logger.error(f"Error parsing detail json: {e}")
                detail_items = {}
            
            result = {
                'status': 'OK',
                'basis': basis_info,
                'detail': detail_items
            }
            
            # 캐시 저장
            HospitalCache.objects.update_or_create(
                cache_key=cache_key,
                defaults={'data': result, 'created_at': timezone.now()}
            )
            
            return JsonResponse(result)
        else:
            return JsonResponse({'status': 'ERROR', 'message': f'HIRA Detail API Error: {detail_res.status_code}'}, status=detail_res.status_code)
            
    except Exception as e:
        logger.error(f"Hospital Detail API Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)


@csrf_exempt
def hospital_list_proxy(request):
    """
    건강보험심사평가원 병원 목록 조회 (위치 기반, 반경 검색)
    xPos: 경도 (Longitude)
    yPos: 위도 (Latitude)
    radius: 반경 (미터)
    """
    import requests
    import json
    
    x = request.GET.get('x') # 경도
    y = request.GET.get('y') # 위도
    radius = request.GET.get('radius', '3000') # 기본 3km
    
    if not x or not y:
        return JsonResponse({'status': 'ERROR', 'message': 'Coordinates (x, y) are required'}, status=400)
        
    # 올바른 키 사용 (Hex Key) - 사용자 제공 키로 고정
    api_key = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    
    url = "https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
    
    params = {
        'serviceKey': api_key,
        'pageNo': '1',
        'numOfRows': '100', # 한 번에 최대 100개
        '_type': 'json',
        'xPos': x,
        'yPos': y,
        'radius': radius
    }
    
    try:
        logger.info(f"Searching Hospitals (Radius): x={x}, y={y}, r={radius}")
        res = requests.get(url, params=params, timeout=10)
        
        if res.status_code == 200:
            try:
                data = res.json()
                body = data.get('response', {}).get('body', {})
                items_container = body.get('items')
                
                # Items가 문자열("")이거나 None인 경우 처리
                if not isinstance(items_container, dict):
                    items = []
                else:
                    items = items_container.get('item', [])
                    if isinstance(items, dict):
                        items = [items]
                
                if isinstance(items, dict):
                    items = [items]
                    
                # 필요한 데이터만 정제하여 반환 (좌표 포함)
                results = []
                for item in items:
                    # 좌표 필드 확인 (XPos/YPos 대소문자 불확실하므로 모두 시도)
                    # HIRA V2 API: XPos(경도), YPos(위도) 사용 확인됨
                    lng = item.get('XPos') or item.get('xPos')
                    lat = item.get('YPos') or item.get('yPos')
                    
                    if lng and lat:
                        results.append({
                            'ykiho': item.get('ykiho'),
                            'yadmNm': item.get('yadmNm'), # 병원명
                            'clCdNm': item.get('clCdNm'), # 종별
                            'addr': item.get('addr'),     # 주소
                            'telno': item.get('telno'),   # 전화번호
                            'lat': lat,
                            'lng': lng,
                            'drTotCnt': item.get('drTotCnt') or item.get('drtotcnt'), # 의사수 (대소문자 대응)
                            'estbDd': item.get('estbDd') or item.get('estbdd'), # 개설일자 (대소문자 대응)
                            'hospUrl': item.get('hospUrl')
                        })
                        
                return JsonResponse({
                    'status': 'OK',
                    'count': len(results),
                    'items': results
                })
                
            except Exception as e:
                logger.error(f"Hospital List JSON Parse Error: {e}")
                return JsonResponse({'status': 'ERROR', 'message': 'Invalid API Response'}, status=500)
        else:
            return JsonResponse({'status': 'ERROR', 'message': f'API Error: {res.status_code}'}, status=res.status_code)
            
    except Exception as e:
        logger.error(f"Hospital List API Error: {e}")
        return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)


