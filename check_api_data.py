import requests
import xml.etree.ElementTree as ET

def test_api():
    url = "http://apis.data.go.kr/1613000/RTMSDataSvcIndTrade/getRTMSDataSvcIndTrade"
    # Sigungu code for Busan Sasang-gu is 26530
    params = {
        "serviceKey": "D9/YQ315X8yL6bM6pY8N+P9YfR9YfR9YfR9YfR9YfR9YfR9YfR9YfR9YfR9YfR9YfR9YfR9YfR9YfR9YfR9YfA==", # This looks like a placeholder from previous logs or views.py
        "LAWD_CD": "26530",
        "DEAL_YMD": "202502"
    }
    
    # Actually I should use the key from views.py or the repo. 
    # Let me check views.py for the key.
    pass

if __name__ == "__main__":
    # I will read the service key from views.py first
    pass
