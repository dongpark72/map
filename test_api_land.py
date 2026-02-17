import requests
import urllib.parse
api_key = "eLT4z26DHHohxuW7Xr5twGST/hHnjYc/2xtfGQIHsI8lFJsnC4xoenhYYy36DqfIvyUY12BzmY4/lXHzKRL1/A=="
sigungu_cd = "26440"
month = "202401"
# Land trade API
api_url = "http://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade"
enc_key = urllib.parse.quote(api_key)
url = f"{api_url}?serviceKey={enc_key}&LAWD_CD={sigungu_cd}&DEAL_YMD={month}"
res = requests.get(url)
print(f"Land Status: {res.status_code}")
if "<item>" in res.text:
    print("Found Land items!")
else:
    print("No Land items or error.")
    print(res.text[:200])
