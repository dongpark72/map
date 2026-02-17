
import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def test_with_curl():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'
    # Reverting to HTTP as HTTPS is blocked on NAS
    URL = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
    
    # Try different combinations of params
    # 1. Standard curl with quoted params
    # Using -G --data-urlencode is best for curl
    cmd = (
        f"curl -L -m 10 --connect-timeout 5 -G '{URL}' "
        f"--data-urlencode 'serviceKey={KEY}' "
        f"--data-urlencode 'numOfRows=10' "
        f"--data-urlencode 'pageNo=1' "
        f"--data-urlencode 'DPSL_MTD_CD=0001' "
        f"--data-urlencode 'SIDO=서울특별시' "
        f"--data-urlencode 'SGK=강남구' "
        f"-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' "
    )
    
    print(f"Running: {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    print("Response:")
    print(stdout.read().decode())
    print("Stderr:")
    print(stderr.read().decode())
    
    client.close()

if __name__ == "__main__":
    test_with_curl()
