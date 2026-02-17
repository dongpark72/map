import requests
import urllib.parse
api_key = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
sigungu_cd = "26440"
month = "202401"
api_url = "http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade"
enc_key = urllib.parse.quote(api_key)
url = f"{api_url}?serviceKey={enc_key}&LAWD_CD={sigungu_cd}&DEAL_YMD={month}"
res = requests.get(url)
print(f"Status: {res.status_code}")
print(res.text[:200])
