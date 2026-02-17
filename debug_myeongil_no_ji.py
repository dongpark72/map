import requests
from urllib.parse import unquote

key2 = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')
sgg = '11740'
bjd = '10900'
bun = '0056'

url = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
params = {
    'serviceKey': key2,
    'sigunguCd': sgg,
    'bjdongCd': bjd,
    'bun': bun, # NO JI
    'numOfRows': 100
}

print(f"--- Searching all buildings on Bun {bun} (No Ji) ---")
res = requests.get(url, params=params)
if "<item>" in res.text:
    print("SUCCESS: Found items without Ji parameter!")
    # count items
    import xml.etree.ElementTree as ET
    root = ET.fromstring(res.content)
    items = root.findall('.//item')
    print(f"Total items found: {len(items)}")
else:
    print("STILL EMPTY without Ji parameter.")
    print(res.text[:300])
