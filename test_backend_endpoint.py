"""
Test the actual backend endpoint to see what data is returned
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, 'e:\\Gundammap')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gundammap.settings')

import django
django.setup()

from maps.views import building_detail_proxy
from django.test import RequestFactory
import json

# Create a mock request
factory = RequestFactory()

# Test PNU from the image (영도구 동삼동 318-49)
test_pnu = "2644010400103180049"

print(f"Testing backend endpoint with PNU: {test_pnu}")
print("=" * 80)

request = factory.get(f'/proxy/building-detail/?pnu={test_pnu}')
response = building_detail_proxy(request)

# Parse the response
data = json.loads(response.content.decode('utf-8'))

print(f"\nResponse Status: {data.get('status')}")
print(f"\nResponse Data:")
print(json.dumps(data, indent=2, ensure_ascii=False))

if 'data' in data:
    if 'title' in data['data']:
        print(f"\n\nTitle Info Found: {len(data['data']['title'])} fields")
        print(f"Source Type: {data['data']['title'].get('sourceType', 'N/A')}")
    
    if 'floors' in data['data']:
        print(f"\nFloors Data Found: {len(data['data']['floors'])} records")
        if len(data['data']['floors']) > 0:
            print("\nFirst 5 floor records:")
            for idx, floor in enumerate(data['data']['floors'][:5]):
                print(f"  {idx+1}. {floor}")
        else:
            print("  ⚠️ WARNING: floors array is EMPTY!")
    else:
        print("\n  ⚠️ WARNING: 'floors' key not found in response!")

print("\n" + "=" * 80)
