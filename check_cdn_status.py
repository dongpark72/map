import requests
import re

try:
    r = requests.get('https://map.goal-runner.com', timeout=10)
    
    # Check for assets.goal-runner.com
    has_cdn = 'assets.goal-runner.com' in r.text
    print(f"CDN domain (assets.goal-runner.com) found: {has_cdn}")
    print()
    
    # Find all CSS and JS URLs
    css_matches = re.findall(r'href=["\']([^"\']+\.css[^"\']*)["\']', r.text)
    js_matches = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', r.text)
    
    print("CSS Files:")
    for url in css_matches[:5]:
        print(f"  - {url}")
    
    print("\nJS Files:")
    for url in js_matches[:5]:
        print(f"  - {url}")
    
    # Check if any static files use the CDN
    all_static = css_matches + js_matches
    cdn_count = sum(1 for url in all_static if 'assets.goal-runner.com' in url)
    local_count = sum(1 for url in all_static if '/static/' in url)
    
    print(f"\nSummary:")
    print(f"  Total static files found: {len(all_static)}")
    print(f"  Using CDN (assets.goal-runner.com): {cdn_count}")
    print(f"  Using local /static/: {local_count}")
    
except Exception as e:
    print(f"Error: {e}")
