import os

file_path = 'maps/views.py'
new_content = """

def warehouse_proxy(request):
    \"\"\"경기도 물류창고 API 프록시\"\"\"
    import requests
    
    # 파라미터 처리
    sigun_nm = request.GET.get('sigun', '')
    p_index = request.GET.get('page', 1)
    p_size = request.GET.get('size', 1000)
    
    api_key = '11411d4d3b464c10a5fe57edb2917d17'
    url = "https://openapi.gg.go.kr/LogisticsWarehouse"
    
    params = {
        "KEY": api_key,
        "Type": "json",
        "pIndex": p_index,
        "pSize": p_size
    }
    
    if sigun_nm:
        params['SIGUN_NM'] = sigun_nm
        
    try:
        logger.info(f"Fetching Warehouse Data: sigun={sigun_nm}")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            # 그대로 전달
            return JsonResponse(response.json())
        else:
            return JsonResponse({'status': 'ERROR', 'message': f'API Error: {response.status_code}'}, status=response.status_code)
            
    except Exception as e:
        logger.error(f"Warehouse API Error: {e}")
        return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)
"""

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "def warehouse_proxy(request):" not in content:
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully appended warehouse_proxy to maps/views.py")
else:
    print("warehouse_proxy already exists in maps/views.py")
