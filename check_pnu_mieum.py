import requests
import os

address = "부산 강서구 미음동 1576-2"
vworld_key = "F78E51BE-4005-3AFF-91E0-BDDBAC8478D0"
url = f"http://api.vworld.kr/req/address?service=address&request=getcoord&version=2.0&crs=epsg:4326&address={address}&refine=true&simple=false&format=json&type=parcel&key={vworld_key}"

res = requests.get(url)
data = res.json()
print("--- VWorld Parcel Search Result ---")
if data.get('response', {}).get('status') == 'OK':
    parcel = data['response']['result']['items'][0]['address']
    pnu = data['response']['result']['items'][0]['id']
    print(f"Address: {parcel['parcel']}")
    print(f"PNU: {pnu}")
    print(f"Bjdong Code (ext): {pnu[:10]}")
    print(f"Sigungu: {pnu[:5]}, Bjdong: {pnu[5:10]}, Plat: {pnu[10]}, Bun: {pnu[11:15]}, Ji: {pnu[15:19]}")
else:
    print("Search Failed.")
