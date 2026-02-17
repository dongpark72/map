import requests

def test_search(query):
    # Testing search via Kakao/VWorld if possible, but let's just check the PNU for that address
    # Usually I can use the same logic as the app.
    pass

if __name__ == "__main__":
    # Just print the known code for 부산 사상구 감전동
    # 부산: 26, 사상구: 470, 감전동: 10200
    # So PNU should start with 2647010200
    print("Expected prefix: 2647010200")
