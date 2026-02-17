from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import ParcelCache
import requests
import json
import logging
import urllib.parse
import re

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("BeautifulSoup4 not installed. Land info feature will be disabled.")

logger = logging.getLogger(__name__)

# Google Maps API Key가 서버 환경 변수에서 갱신되지 않는 문제를 해결하기 위해 직접 정의합니다.
DIRECT_GOOGLE_KEY = "AIzaSyDQ4i925c2gLuRrqbMgAsWWZ2sy2T6sv8w"

def index(request):
    context = {
        'google_maps_api_key': DIRECT_GOOGLE_KEY, # 환경 변수 대신 직접 정의한 키 사용
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
    
    if not BS4_AVAILABLE:
        return JsonResponse({
            'status': 'ERROR',
            'message': 'BeautifulSoup4가 설치되지 않았습니다. 서버 관리자에게 문의하세요.'
        })
    
    pnu = request.GET.get('pnu')
    if not pnu:
        return JsonResponse({'error': 'PNU is required'}, status=400)
    
    # 0. 캐시 확인 (1시간 유효)
    try:
        from django.utils import timezone
        from datetime import timedelta
        # ParcelCache를 정보 캐시로도 활용하거나 별도 필드 추가 가능 여부 확인
        # 여기서는 단순화를 위해 실시간 처리하되 병렬화에 집중
    except:
        pass

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

        # PNU 보정 로직 (강서구 대저동 등 행정동/법정동 코드 불일치 대응)
        pnus_to_try = [pnu]
        if pnu.startswith('2644010400'):
            alt_pnu = '2644010100' + pnu[10:]
            pnus_to_try.append(alt_pnu)

        # 1. 토지 정보 API (V-World NED - 토지특성)
        def fetch_ned_data():
            try:
                connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
                ned_url = "http://api.vworld.kr/ned/data/getLandCharacteristics"
                ned_key = "98A53FD9-F542-32C4-9589-78A54E531AF7"
                
                for target_pnu in pnus_to_try:
                    # 100건을 가져와서 과거 공시지가까지 확보
                    query = f"{ned_url}^key={ned_key}|pnu={target_pnu}|domain=http://www.eum.go.kr|format=xml|numOfRows=100"
                    res = session.get(connector_url, params={'url': query}, timeout=7)
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
                                        except: pass
                            break # 첫 번째 성공한 PNU에서 멈춤
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
                
                keys_to_try = [
                    "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
                    "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368",
                ]
                
                found_api = False
                recap_found = False
                
                for target_pnu in pnus_to_try:
                    if found_api and recap_found: break
                    
                    sigungu = target_pnu[0:5]
                    bjdong = target_pnu[5:10]
                    platGb = '0' if target_pnu[10] == '1' else '1'
                    bun = str(int(target_pnu[11:15])).zfill(4) 
                    ji = str(int(target_pnu[15:19])).zfill(4)
                    
                    for api_key in keys_to_try:
                        enc_key = urllib.parse.quote(api_key)
                        
                        # 1-1. 총괄표제부 (Recap)
                        if not recap_found:
                            try:
                                q_recap = f"{api_url_recap}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
                                res_recap = session.get(connector_url, params={'url': q_recap}, timeout=5)
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
                            except: pass

                        # 1-2. 일반표제부 (Title)
                        if not found_api:
                            try:
                                q_title = f"{api_url_title}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
                                res_title = session.get(connector_url, params={'url': q_title}, timeout=6)
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
                            except: pass
                
                # 1-3. 층별 개요 API (누락된 동 명칭 보충)
                try:
                    found_dongs = {b.get('동명칭').strip() for b in api_buildings if b.get('동명칭')}
                    for target_pnu in pnus_to_try:
                        sigungu = target_pnu[0:5]; bjdong = target_pnu[5:10]
                        platGb = '0' if target_pnu[10] == '1' else '1'
                        bun = str(int(target_pnu[11:15])).zfill(4); ji = str(int(target_pnu[15:19])).zfill(4)
                        for api_key in keys_to_try:
                            enc_key = urllib.parse.quote(api_key)
                            try:
                                q_flr = f"{api_url_flr}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
                                res_flr = session.get(connector_url, params={'url': q_flr}, timeout=6)
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
                            except: pass
                except: pass

                # 건물 정렬 (총괄표제부 우선, 그 외 동명칭 오름차순 - 숫자우선)
                def bld_sort_key(b):
                    name = b.get('동명칭', '').strip()
                    # 1순위: 총괄표제부
                    if '총괄' in name or name == '표제부':
                        return (0, 0, name)
                    
                    # 2순위: 숫자로 시작하는 동명칭 (예: 1동, 101동)
                    m = re.match(r'^(\d+)', name)
                    if m:
                        return (1, int(m.group(1)), name)
                    
                    # 3순위: 기타 (가나다순)
                    return (2, 0, name)

                api_buildings.sort(key=bld_sort_key)

                structured_data['buildings'] = api_buildings
            except Exception as e:
                logger.error(f"Building API Error: {e}")

        # 병렬 실행 (웹크롤링 제거, 오직 API만 사용)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(fetch_ned_data),
                executor.submit(fetch_building_info)
            ]
            concurrent.futures.wait(futures)

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
    if not pnu:
        return JsonResponse({'error': 'PNU is required'}, status=400)
    
    # PNU 보정
    pnus_to_try = [pnu]
    if pnu.startswith('2644010400'):
        alt_pnu = '2644010100' + pnu[10:]
        pnus_to_try.append(alt_pnu)

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
    
    # API Endpoints
    api_url_recap = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
    api_url_title = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
    
    keys_to_try = [
        "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A==",
        "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368",
    ]

    result_data = {
        'recap': {}, 
        'titles': []
    }

    try:
        working_key = keys_to_try[0]
        recap_item = None
        title_items = []

        # 1. 정보 수집
        found_any = False
        
        for target_pnu in pnus_to_try:
            if found_any: break

            # PNU 파싱
            sigungu = target_pnu[0:5]
            bjdong = target_pnu[5:10]
            pnu_land_type = target_pnu[10]
            
            # PNU 대지구분(1,2) -> API platGbCd(0,1) 변환
            if pnu_land_type == '1':
                platGb = '0'
            elif pnu_land_type == '2':
                platGb = '1'
            else:
                platGb = '0' # Default
            
            bun = str(int(target_pnu[11:15])).zfill(4)
            ji = str(int(target_pnu[15:19])).zfill(4)

            for key in keys_to_try:
                enc_key = urllib.parse.quote(key)
                
                # 1-1. 총괄표제부 (Recap) 조회
                # numOfRows=1, pageNo=1 (총괄은 보통 1개)
                try:
                    q_recap = f"{api_url_recap}^serviceKey={enc_key}|numOfRows=1|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
                    res_recap = session.get(connector_url, params={'url': q_recap}, timeout=5)
                    if res_recap.status_code == 200 and "<item>" in res_recap.text:
                        root = ET.fromstring(res_recap.text)
                        items = root.findall('.//item')
                        if items:
                            recap_item = items[0] # 첫번째 항목 사용
                            found_any = True
                except Exception as e:
                    logger.error(f"Recap Error: {e}")

                # 1-2. 일반표제부 (Title) 목록 조회
                try:
                    q_title = f"{api_url_title}^serviceKey={enc_key}|numOfRows=999|pageNo=1|sigunguCd={sigungu}|bjdongCd={bjdong}|platGbCd={platGb}|bun={bun}|ji={ji}"
                    res_title = session.get(connector_url, params={'url': q_title}, timeout=6)
                    if res_title.status_code == 200 and "<item>" in res_title.text:
                        items = ET.fromstring(res_title.text).findall('.//item')
                        if items:
                            title_items.extend(items)
                            if not found_any: found_any = True # Recap이 없어도 Title이 있으면 성공으로 간주
                except Exception as e:
                    logger.error(f"Title Error: {e}")
                
                if found_any:
                    working_key = key
                    break
        
        # 2. 데이터 매핑
        def get_t(it, tag):
            if it is None: return ''
            el = it.find(tag); return el.text.strip() if el is not None and el.text else ''
        
        def format_date(d):
            if not d or len(d) != 8: return d
            return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
        
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
                '구조': get_t(it, 'strctCdNm'), # + ' ' + get_t(it, 'roofCdNm'), # 이미지상 구조/지붕 합쳐져 있음
                '지붕': get_t(it, 'roofCdNm'),
                '층수': f"{get_t(it, 'ugrndFlrCnt')}/{get_t(it, 'grndFlrCnt')}",
                '용도': get_t(it, 'mainPurpsCdNm'),
                '면적': get_t(it, 'totArea'), # 연면적
                'PK': get_t(it, 'mgmBldrgstPk')
            })

        # 정렬: 숫자우선 오름차순
        def bld_sort_key(b):
            name = b['명칭']
            m = re.match(r'^(\d+)', name)
            if m: return (0, int(m.group(1)), name)
            return (1, 0, name)
        
        mapped_titles.sort(key=bld_sort_key)
        result_data['titles'] = mapped_titles

        return JsonResponse({'status': 'OK', 'data': result_data})

    except Exception as e:
        logger.error(f"Building Detail Error: {e}")
        import traceback
        return JsonResponse({'status': 'ERROR', 'message': f"{str(e)}\n{traceback.format_exc()}"})



