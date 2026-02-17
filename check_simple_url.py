
import paramiko
import os
import time

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_connectivity():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        print("Connected to SSH.")
        
        # Target URL based on User Screenshot
        url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
        print(f"\nChecking URL: {url}")
        
        # Test CURL from Host (NAS) to verify network basics
        print("[NAS Host] Testing connectivity...")
        # Just head check with 5s timeout
        cmd_host = f"curl -I --connect-timeout 5 {url}"
        stdin, stdout, stderr = client.exec_command(cmd_host)
        out = stdout.read().decode()
        err = stderr.read().decode()
        print(f"Result:\n{out}\n{err}")
        
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    check_connectivity()
