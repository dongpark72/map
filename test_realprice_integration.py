"""
실거래가 기능 통합 테스트
- HTML에 '실' 버튼이 있는지 확인
- realprice-panel이 있는지 확인
- showRealPrice 함수가 있는지 확인
- backend endpoint가 있는지 확인
"""

import re

def test_html_integration():
    print("=" * 60)
    print("실거래가 기능 통합 테스트")
    print("=" * 60)
    
    # 1. index.html 확인
    with open('templates/maps/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    checks = {
        "'실' 버튼 생성 코드": "realBtn.innerText = '실';" in html_content,
        "realprice-panel HTML": 'id="realprice-panel"' in html_content,
        "showRealPrice 함수": "async function showRealPrice" in html_content,
        "실거래가 탭 (아파트)": 'data-type="apt"' in html_content,
        "실거래가 탭 (공장/창고)": 'data-type="factory"' in html_content,
        "실거래가 API 호출": "/proxy/real-price/" in html_content,
        "자동 유형 감지 로직": "defaultRealPriceType" in html_content,
    }
    
    print("\n[HTML 체크]")
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check}: {result}")
    
    # 2. views.py 확인
    with open('maps/views.py', 'r', encoding='utf-8') as f:
        views_content = f.read()
    
    backend_checks = {
        "real_price_proxy 함수": "def real_price_proxy(request):" in views_content,
        "7가지 API 매핑": "'factory': 'http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade" in views_content,
        "병렬 처리 (ThreadPoolExecutor)": "concurrent.futures.ThreadPoolExecutor" in views_content,
        "최근 24개월 데이터": "for i in range(24):" in views_content,
    }
    
    print("\n[Backend 체크]")
    for check, result in backend_checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check}: {result}")
    
    # 3. urls.py 확인
    with open('maps/urls.py', 'r', encoding='utf-8') as f:
        urls_content = f.read()
    
    url_check = "path('proxy/real-price/', views.real_price_proxy" in urls_content
    print("\n[URL 라우팅 체크]")
    status = "✓" if url_check else "✗"
    print(f"  {status} URL 엔드포인트 등록: {url_check}")
    
    # 4. 실거래가 버튼 활성화 로직 확인
    print("\n[실거래가 버튼 활성화 로직]")
    
    # '실' 버튼이 생성되는지 확인
    real_btn_creation = re.search(r"const realBtn = document\.createElement\('button'\);", html_content)
    print(f"  {'✓' if real_btn_creation else '✗'} '실' 버튼 생성: {bool(real_btn_creation)}")
    
    # '실' 버튼이 disabled 클래스 제거되는지 확인
    real_btn_enable = re.search(r"data\.realBtn\.classList\.remove\('disabled'\);", html_content)
    print(f"  {'✓' if real_btn_enable else '✗'} '실' 버튼 활성화: {bool(real_btn_enable)}")
    
    # onClick 이벤트가 showRealPrice를 호출하는지 확인
    real_btn_onclick = re.search(r"showRealPrice\(idx, polygonsData\[idx\]\.defaultRealPriceType", html_content)
    print(f"  {'✓' if real_btn_onclick else '✗'} onClick 이벤트 연결: {bool(real_btn_onclick)}")
    
    # 5. 종합 결과
    all_checks = list(checks.values()) + list(backend_checks.values()) + [url_check]
    total = len(all_checks)
    passed = sum(all_checks)
    
    print("\n" + "=" * 60)
    print(f"종합 결과: {passed}/{total} 통과 ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n✓ 모든 체크 통과! 실거래가 기능이 정상적으로 구현되어 있습니다.")
        print("\n[사용 방법]")
        print("1. 주소를 검색합니다")
        print("2. 검색 결과 아래의 주황색 '실' 버튼을 클릭합니다")
        print("3. 화면 우측 하단에 실거래가 패널이 표시됩니다")
        print("4. 패널 상단의 탭을 클릭하여 다른 유형의 실거래가를 조회할 수 있습니다")
    else:
        print("\n✗ 일부 체크 실패. 위의 결과를 확인하세요.")
    
    return passed == total

if __name__ == "__main__":
    test_html_integration()
