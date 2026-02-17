import requests
import urllib.parse
api_key = "e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368"
sigungu_cd = "26440"
month = "202401"
api_url = "http://apis.data.go.kr/1613000/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade"
enc_key = urllib.parse.quote(api_key)
query = f"{api_url}^serviceKey={enc_key}|LAWD_CD={sigungu_cd}|DEAL_YMD={month}"
connector_url = "https://www.eum.go.kr/dataapis/UrlConnector.jsp"
res = requests.get(connector_url, params={'url': query})
print(f"Proxy Status: {res.status_code}")
print("Response text (first 500):")
print(res.text[:500])
