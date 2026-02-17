import requests
from urllib.parse import unquote

service_key = unquote('e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368')
url = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

# 호수(ji) 없이 번지만 검색하여 어떤 데이터가 있는지 확인
params = {
    'serviceKey': service_key,
    'sigunguCd': '26440',
    'bjdongCd': '10600',
    'platGbCd': '0',
    'bun': '1576',
    'numOfRows': 100
}

res = requests.get(url, params=params)
import xml.etree.ElementTree as ET
root = ET.fromstring(res.content)
items = root.findall('.//item')

print(f"Total items for Bjdong Code 10600, Bun 1576: {len(items)}")
for it in items:
    bld_nm = it.find('bldNm').text if it.find('bldNm') is not None else 'No Name'
    bun_val = it.find('bun').text
    ji_val = it.find('ji').text
    main_prpos = it.find('mainPrposCdNm').text if it.find('mainPrposCdNm') is not None else 'No Purpose'
    print(f"- {bld_nm} | {bun_val}-{ji_val} | {main_prpos}")
