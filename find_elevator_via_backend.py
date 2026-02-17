import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, 'e:\\Gundammap')

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gundammap.settings')
import django
django.setup()

from maps.views import building_detail_proxy
from django.test import RequestFactory

def test_pnu(pnu):
    print(f"Testing PNU: {pnu}")
    rf = RequestFactory()
    request = rf.get(f'/proxy/building-detail/?pnu={pnu}')
    response = building_detail_proxy(request)
    data = json.loads(response.content.decode('utf-8'))
    
    if data.get('status') == 'OK':
        recap = data.get('data', {}).get('recap', {})
        elev = recap.get('승강기', 'N/A')
        print(f"  Elevator Result: {elev}")
        if any(c.isdigit() and c != '0' for c in elev):
            print(f"  SUCCESS! Found numeric elevator info: {elev}")
            return True
    else:
        print(f"  Error: {data.get('message')}")
    return False

# PNUs
pnus = [
    "1168010100108250013", # Gangnam Stn
    "2644010100106000000", # Gangseo-gu Office area?
    "1165010100113200001",
    "2623010100105030015",
]

for p in pnus:
    if test_pnu(p):
        print(f"\nWINNER: {p}")
        break
