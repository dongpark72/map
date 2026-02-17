import requests

try:
    r = requests.get('https://map.goal-runner.com/portal/', timeout=10)
    
    # Check for inline styles and scripts
    print("="*80)
    print("Analyzing HTML structure:")
    print("="*80)
    
    # Count style and script tags
    import re
    style_tags = len(re.findall(r'<style[^>]*>', r.text))
    script_tags = len(re.findall(r'<script[^>]*>', r.text))
    link_tags = len(re.findall(r'<link[^>]*>', r.text))
    
    print(f"<style> tags: {style_tags}")
    print(f"<script> tags: {script_tags}")
    print(f"<link> tags: {link_tags}")
    
    # Look for {% static %} template tags (should be rendered)
    static_tag_pattern = r'{%\s*static\s+["\']([^"\']+)["\']\s*%}'
    static_tags = re.findall(static_tag_pattern, r.text)
    
    print(f"\nUnrendered {{% static %}} tags found: {len(static_tags)}")
    if static_tags:
        print("WARNING: Template tags not rendered!")
        for tag in static_tags[:5]:
            print(f"  - {tag}")
    
    # Search for any reference to static files
    print("\n" + "="*80)
    print("Searching for static file patterns:")
    print("="*80)
    
    # Look for common patterns
    patterns = [
        (r'href=["\']([^"\']*static[^"\']*)["\']', 'href with "static"'),
        (r'src=["\']([^"\']*static[^"\']*)["\']', 'src with "static"'),
        (r'href=["\']([^"\']*assets\.goal-runner\.com[^"\']*)["\']', 'href with CDN'),
        (r'src=["\']([^"\']*assets\.goal-runner\.com[^"\']*)["\']', 'src with CDN'),
        (r'url\(["\']?([^"\'()]*static[^"\'()]*)["\']?\)', 'CSS url() with static'),
    ]
    
    for pattern, desc in patterns:
        matches = re.findall(pattern, r.text, re.IGNORECASE)
        if matches:
            print(f"\n{desc}: {len(matches)} found")
            for match in matches[:3]:
                print(f"  - {match}")
    
    # Check first 3000 chars for clues
    print("\n" + "="*80)
    print("HTML Head section (first 3000 chars):")
    print("="*80)
    head_match = re.search(r'<head>(.*?)</head>', r.text, re.DOTALL | re.IGNORECASE)
    if head_match:
        head_content = head_match.group(1)[:3000]
        print(head_content)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
