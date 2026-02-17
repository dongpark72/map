import requests

try:
    r = requests.get('https://map.goal-runner.com', timeout=10)
    print(f"Status Code: {r.status_code}")
    print(f"Content Length: {len(r.text)}")
    print("\n" + "="*80)
    print("HTML Content (first 2000 characters):")
    print("="*80)
    print(r.text[:2000])
    print("\n" + "="*80)
    print("Checking for specific patterns:")
    print("="*80)
    print(f"Contains 'static': {'static' in r.text}")
    print(f"Contains 'assets.goal-runner.com': {'assets.goal-runner.com' in r.text}")
    print(f"Contains 'map_app.css': {'map_app.css' in r.text}")
    print(f"Contains 'map_app.js': {'map_app.js' in r.text}")
    
except Exception as e:
    print(f"Error: {e}")
