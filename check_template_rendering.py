import requests

try:
    r = requests.get('https://map.goal-runner.com/portal/', timeout=10)
    
    # Search for {% static %} tags (should be rendered to actual URLs)
    print("="*80)
    print("Checking for template rendering:")
    print("="*80)
    
    # Check if {% static %} tags are present (unrendered)
    if '{% static' in r.text:
        print("[ERROR] Template tags are NOT being rendered!")
        print("Found unrendered tags in HTML")
    else:
        print("[OK] No unrendered template tags found")
    
    # Check for <link> and <script> tags
    import re
    link_tags = re.findall(r'<link[^>]*>', r.text)
    script_tags = re.findall(r'<script[^>]*src=[^>]*>', r.text)
    
    print(f"\n<link> tags found: {len(link_tags)}")
    for tag in link_tags[:5]:
        print(f"  {tag}")
    
    print(f"\n<script> tags with src found: {len(script_tags)}")
    for tag in script_tags[:5]:
        print(f"  {tag}")
    
    # Look for the specific pattern in head
    print("\n" + "="*80)
    print("Searching for CSS/JS references in <head>:")
    print("="*80)
    head_match = re.search(r'<head>(.*?)</head>', r.text, re.DOTALL | re.IGNORECASE)
    if head_match:
        head = head_match.group(1)
        # Look for map_app references
        if 'map_app.css' in head:
            print("[FOUND] map_app.css reference in head")
            # Extract the line
            for line in head.split('\n'):
                if 'map_app.css' in line:
                    print(f"  Line: {line.strip()[:200]}")
        else:
            print("[NOT FOUND] map_app.css reference")
            
        if 'map_app.js' in head or 'map_app.js' in r.text:
            print("[FOUND] map_app.js reference")
            for line in r.text.split('\n'):
                if 'map_app.js' in line:
                    print(f"  Line: {line.strip()[:200]}")
                    break
        else:
            print("[NOT FOUND] map_app.js reference")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
