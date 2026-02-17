import time
import requests

print("Waiting 20 seconds for containers to fully restart...")
time.sleep(20)

print("\nChecking CDN application...")
try:
    r = requests.get('https://map.goal-runner.com/portal/', timeout=10)
    
    print(f"Status Code: {r.status_code}")
    print(f"Content Length: {len(r.text)}")
    
    # Check for CDN domain
    has_cdn = 'assets.goal-runner.com' in r.text
    print(f"\n[{'SUCCESS' if has_cdn else 'FAIL'}] CDN domain (assets.goal-runner.com) found: {has_cdn}")
    
    # Find CSS and JS references
    import re
    css_matches = re.findall(r'href=["\']([^"\']+\.css[^"\']*)["\']', r.text)
    js_matches = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', r.text)
    
    print(f"\nCSS Files ({len(css_matches)}):")
    for url in css_matches:
        cdn_marker = " [CDN]" if 'assets.goal-runner.com' in url else ""
        print(f"  - {url}{cdn_marker}")
    
    print(f"\nJS Files ({len(js_matches)}):")
    for url in js_matches:
        cdn_marker = " [CDN]" if 'assets.goal-runner.com' in url else ""
        print(f"  - {url}{cdn_marker}")
    
    # Summary
    all_static = css_matches + js_matches
    cdn_count = sum(1 for url in all_static if 'assets.goal-runner.com' in url)
    
    print(f"\n{'='*80}")
    print("SUMMARY:")
    print(f"{'='*80}")
    print(f"Total static files: {len(all_static)}")
    print(f"Using CDN: {cdn_count}")
    print(f"CDN Status: {'✓ ENABLED' if cdn_count > 0 else '✗ NOT ENABLED'}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
