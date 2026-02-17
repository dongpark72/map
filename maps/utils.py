"""
Utility functions for Gundammap project
"""
import re
from typing import Dict, List


def parse_pnu(pnu: str) -> Dict[str, str]:
    """PNU를 API 파라미터로 변환
    
    Args:
        pnu: 19자리 PNU 코드
        
    Returns:
        API 파라미터 딕셔너리
        
    Raises:
        ValueError: PNU 형식이 올바르지 않은 경우
    """
    if not pnu or len(pnu) != 19:
        raise ValueError(f"Invalid PNU length: {pnu}")
    
    return {
        'sigunguCd': pnu[0:5],
        'bjdongCd': pnu[5:10],
        'platGbCd': '0' if pnu[10] == '1' else '1',
        'bun': str(int(pnu[11:15])).zfill(4),
        'ji': str(int(pnu[15:19])).zfill(4)
    }


def get_pnu_alternatives(pnu: str) -> List[str]:
    """PNU 대체 코드 생성 (행정동/법정동 불일치 대응)
    
    Args:
        pnu: 원본 PNU
        
    Returns:
        시도할 PNU 목록
    """
    pnus = [pnu]
    
    # 강서구 대저동 (행정동 코드 -> 법정동 코드)
    if pnu.startswith('2644010400'):
        pnus.append('2644010100' + pnu[10:])
    
    return pnus


def sort_buildings(buildings: List[dict], name_key: str = '동명칭') -> List[dict]:
    """건물 목록 정렬 (총괄표제부 우선, 숫자 오름차순)
    
    Args:
        buildings: 건물 정보 리스트
        name_key: 정렬 기준 키
        
    Returns:
        정렬된 건물 리스트
    """
    def sort_key(b):
        name = b.get(name_key, '').strip()
        
        # 총괄표제부 우선
        if '총괄' in name or name == '표제부':
            return (0, 0, name)
        
        # 숫자로 시작하는 동명칭
        m = re.match(r'^(\d+)', name)
        if m:
            return (1, int(m.group(1)), name)
        
        # 기타 (가나다순)
        return (2, 0, name)
    
    return sorted(buildings, key=sort_key)


def validate_pnu(pnu: str) -> bool:
    """PNU 형식 검증
    
    Args:
        pnu: 검증할 PNU
        
    Returns:
        유효 여부
    """
    if not pnu:
        return False
    
    # 19자리 숫자인지 확인
    if not re.match(r'^\d{19}$', pnu):
        return False
    
    # 대지구분 코드 검증 (1: 대지, 2: 산)
    if pnu[10] not in ['1', '2']:
        return False
    
    return True


def format_date(date_str: str) -> str:
    """날짜 문자열 포맷팅 (YYYYMMDD -> YYYY-MM-DD)
    
    Args:
        date_str: 8자리 날짜 문자열
        
    Returns:
        포맷팅된 날짜 문자열
    """
    if not date_str or len(date_str) != 8:
        return date_str
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"


def normalize_bjdong_name(name: str) -> str:
    """법정동명 정규화 (공란 제거, 한글 정규화 등)
    
    Args:
        name: 원본 법정동명
        
    Returns:
        정규화된 법정동명
    """
    if not name:
        return ""
    
    # 1. 유니코드 정규화 (NFC로 통일)
    import unicodedata
    name = unicodedata.normalize('NFC', name)
    
    # 2. 모든 공백 제거
    name = "".join(name.split())
    
    # 3. 특수문자 및 불필요한 문자 제거 (필요시 추가)
    
    return name
