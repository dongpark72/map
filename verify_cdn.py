import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

def verify_cdn(url, cdn_domain):
    try:
        r = requests.get(url, timeout=10)
        print(f"Status Code: {r.status_code}")
        
        if r.status_code != 200:
            print(f"❌ Error: HTTP {r.status_code}")
            return False
        
        # CDN 도메인 확인
        has_cdn = cdn_domain in r.text
        print(f"\n{'✅' if has_cdn else '❌'} CDN domain ({cdn_domain}) found: {has_cdn}")
        
        # CSS/JS 파일 찾기
        css_matches = re.findall(r'href=["\']([^\"\']+ \.css[^\"\']*)["\']', r.text)
        js_matches = re.findall(r'src=["\']([^\"\']+ \.js[^\"\']*)["\']', r.text)
        
        print(f"\nCSS Files ({len(css_matches)}):")
        for url in css_matches:
            cdn_marker = " [CDN]" if cdn_domain in url else ""
            print(f"  - {url}{cdn_marker}")
        
        print(f"\nJS Files ({len(js_matches)}):")
        for url in js_matches:
            cdn_marker = " [CDN]" if cdn_domain in url else ""
            print(f"  - {url}{cdn_marker}")
        
        # 요약
        all_static = css_matches + js_matches
        cdn_count = sum(1 for url in all_static if cdn_domain in url)
        
        print(f"\n{'='*80}")
        print(f"Total static files: {len(all_static)}")
        print(f"Using CDN: {cdn_count}")
        print(f"CDN Status: {'✅ ENABLED' if cdn_count > 0 else '❌ NOT ENABLED'}")
        
        return cdn_count > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # .env에서 설정 읽기
    cdn_domain = os.getenv('R2_CUSTOM_DOMAIN', 'assets.goal-runner.com')
    cdn_domain = cdn_domain.replace('https://', '').replace('http://', '')
    
    # 사용자에게 URL 입력 요청
    url = input("검증할 웹사이트 URL을 입력하세요 (예: https://map.goal-runner.com/portal/): ").strip()
    
    if url:
        verify_cdn(url, cdn_domain)
    else:
        print("❌ URL을 입력해주세요")
