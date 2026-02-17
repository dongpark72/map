from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import ParcelCache, LandInfoCache
from .utils import validate_pnu, parse_pnu, get_pnu_alternatives, sort_buildings, format_date
import requests
import json
import logging
import urllib.parse
import os

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
    }
    return render(request, 'maps/index.html', context)

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

    domain = 'http://175.126.187.59:8000/'
    
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

