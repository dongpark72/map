import requests

try:
    # Try to access the portal page
    r = requests.get('https://map.goal-runner.com/portal/', timeout=10, allow_redirects=False)
    print(f"Status Code: {r.status_code}")
    print(f"Content Length: {len(r.text)}")
    
    if r.status_code == 302 or r.status_code == 301:
        print(f"Redirect Location: {r.headers.get('Location', 'N/A')}")
    
    print("\n" + "="*80)
    print("Checking for CDN and static files:")
    print("="*80)
    print(f"Contains 'static': {'static' in r.text}")
    print(f"Contains 'assets.goal-runner.com': {'assets.goal-runner.com' in r.text}")
    print(f"Contains 'map_app.css': {'map_app.css' in r.text}")
    print(f"Contains 'map_app.js': {'map_app.js' in r.text}")
    
    # Find static file references
    import re
    css_matches = re.findall(r'href=["\']([^"\']+\.css[^"\']*)["\']', r.text)
    js_matches = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', r.text)
    
    if css_matches:
        print("\nCSS Files found:")
        for url in css_matches[:10]:
            print(f"  - {url}")
    
    if js_matches:
        print("\nJS Files found:")
        for url in js_matches[:10]:
            print(f"  - {url}")
    
    # Check for CDN usage
    all_static = css_matches + js_matches
    cdn_files = [url for url in all_static if 'assets.goal-runner.com' in url]
    local_files = [url for url in all_static if '/static/' in url or url.startswith('/')]
    
    print(f"\n" + "="*80)
    print("Summary:")
    print("="*80)
    print(f"Total static files: {len(all_static)}")
    print(f"CDN files (assets.goal-runner.com): {len(cdn_files)}")
    print(f"Local files: {len(local_files)}")
    
    if cdn_files:
        print("\nCDN Files:")
        for url in cdn_files:
            print(f"  ✓ {url}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
