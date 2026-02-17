import requests
import xml.etree.ElementTree as ET

pnu = "2644010100107900000"
key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
sigungu = pnu[0:5]
bjdong = pnu[5:10]
platGb = '0' if pnu[10] == '1' else '1'
bun = str(int(pnu[11:15])).zfill(4)
ji = str(int(pnu[15:19])).zfill(4)

base_params = f"serviceKey={key}&sigunguCd={sigungu}&bjdongCd={bjdong}&platGbCd={platGb}&bun={bun}&ji={ji}&numOfRows=200"

print(f"--- Deep Diagnose PNU: {pnu} ---")

# 1. Recap Detail
url_recap = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrRecapTitleInfo"
try:
    res = requests.get(url_recap + "?" + base_params, timeout=5)
    root = ET.fromstring(res.text)
    items = root.findall('.//item')
    if items:
        item = items[0]
        mainCnt = item.find('mainBldCnt').text if item.find('mainBldCnt') is not None else '0'
        atchCnt = item.find('atchBldCnt').text if item.find('atchBldCnt') is not None else '0'
        totArea = item.find('totArea').text if item.find('totArea') is not None else '0'
        print(f"[Recap] Main Bld Count: {mainCnt}, Atch Bld Count: {atchCnt}, Total Area: {totArea}")
    else:
        print("[Recap] No items found.")
except Exception as e:
    print(f"[Recap] Error: {e}")

# 2. Expos (Group Building / Jeonyu)
url_expos = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrExposPubuseAreaInfo"
try:
    res = requests.get(url_expos + "?" + base_params, timeout=5)
    root = ET.fromstring(res.text)
    items = root.findall('.//item')
    print(f"[Expos/Group] Count: {len(items)}")
    dongs = set()
    for item in items:
        d = item.find('dongNm')
        if d is not None and d.text: dongs.add(d.text)
    if dongs:
        print(f"  -> Dongs in Expos: {dongs}")
except Exception as e:
    print(f"[Expos] Error: {e}")

# 3. Title (General) again to check 'atchBldCnt' per building? No.
# Just clarify if we missed anything.
