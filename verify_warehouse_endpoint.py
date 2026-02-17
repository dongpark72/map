import requests
import json

def verify_endpoint():
    # The container maps 80 to 8002 usually, or let's try 8000/8002
    # Previous code used 8000 internally, but external might be 8002 based on user history?
    # View `check_server_status.py` in Step 10... it didn't specify port.
    # The `check_server_deployment.py` mentioned `domain = 'http://175.126.187.59:8000/'` in views.py context.
    # But often external access is 8002. Let's try both or just 8000 if that's what Django runs on.
    # Actually, `docker-compose.yml` (Step 4) map?
    
    # Try 8002 first as per history "external forwarded port 8002"
    url = "http://175.126.187.59:8002/maps/proxy/warehouse/"
    # Wait, maps app has `path('', include('maps.urls'))` in main urls? 
    # Usually `gundammap` project urls has `path('maps/', include('maps.urls'))` or just `path('', ...)`?
    # In `check_server_deployment.py` Step 6 output: `cat .../maps/urls.py` showed `path('proxy/warehouse/', ...)` inside `maps/views.py`... no, that file is `maps/urls.py`.
    # Does the project route map to `/` or `/maps/`?
    # Let's check `gundammap/settings.py` or main `urls.py`... 
    # But simply looking at `maps/urls.py` (Step 16) it has `path('', views.index, name='index')`.
    # So if I access root, I get index.
    # So likely it is mounted at `/` or `/maps/`.
    # If mounted at `/`, then `http://.../proxy/warehouse/`.
    
    urls_to_try = [
        "http://175.126.187.59:8002/proxy/warehouse/",
        "http://175.126.187.59:8000/proxy/warehouse/",
        "http://175.126.187.59:8002/maps/proxy/warehouse/"
    ]
    
    params = {
        "sigun": "용인시",
        "page": 1,
        "size": 5
    }
    
    for u in urls_to_try:
        try:
            print(f"Trying {u}...")
            res = requests.get(u, params=params, timeout=5)
            print(f"Status: {res.status_code}")
            if res.status_code == 200:
                print("Response Snippet:", res.text[:200])
                break
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    verify_endpoint()
