
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
        
        # 1. Check Container Name
        print("\n[Step 1] Checking running containers...")
        stdin, stdout, stderr = client.exec_command("echo " + PASS + " | sudo -S docker ps --format '{{.Names}}'")
        containers = stdout.read().decode().strip().split('\n')
        print(f"Containers found: {containers}")
        
        target_container = None
        for c in containers:
            if 'gundammap' in c and 'web' in c:
                target_container = c
                break
        
        if not target_container:
            print("Could not find gundammap web container.")
            target_container = 'gundammap-web-1' # Fallback guess
            
        print(f"Target Container: {target_container}")
        
        # 2. Test CURL from Host (NAS)
        print("\n[Step 2] Testing CURL from NAS Host...")
        url = "http://openapi.onbid.co.kr/openapi/services/KamcoPblsalThingInquireSvc/getKamcoPbctCltrList"
        cmd_host = f"curl -I --connect-timeout 5 {url}"
        stdin, stdout, stderr = client.exec_command(cmd_host)
        out = stdout.read().decode()
        err = stderr.read().decode()
        print(f"Host Curl Result:\n{out}\n{err}")
        
        # 3. Upload and Run Diagnose Script
        print("\n[Step 3] Uploading and Running Diagnose Script...")
        
        diag_code = """
import requests
import sys
import xml.dom.minidom

# Configuration
URL_UNIFY = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
URL_KAMCO = "http://openapi.onbid.co.kr/openapi/services/KamcoPblsalThingInquireSvc/getKamcoPbctCltrList"
KEY = 'e273fd424ad56ffe02f2e043da6cb2c34f37f9a4d7c18f3daeea70b551099368'

def print_response(title, response):
    print(f"\\n--- {title} ---")
    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")
    try:
        if response.text.strip().startswith('<'):
             # Simple formatting
             import xml.dom.minidom
             dom = xml.dom.minidom.parseString(response.text)
             print(dom.toprettyxml(indent="  ")[:1000])
        else:
             print(response.text[:500])
    except:
        print(response.text[:500])

def test_unify():
    # Mimic Chrome on Windows 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }
    
    params = {
        'serviceKey': KEY,
        'numOfRows': '10',
        'pageNo': '1',
        'SIDO': '서울특별시',
        'SGK': '강남구'
    }
    try:
        r = requests.get(URL_UNIFY, params=params, headers=headers, timeout=10)
        print_response("Testing getUnifyUsageCltr (Unified Info)", r)
    except Exception as e:
        print(f"Unify Test Failed: {e}")

def test_kamco():
    # Mimic Chrome on Windows 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }

    params = {
        'serviceKey': KEY,
        'numOfRows': '10',
        'pageNo': '1',
        'DPSL_MTD_CD': '0001', # Sale
        'SIDO': '서울특별시',
        'SGK': '강남구'
    }
    try:
        r = requests.get(URL_KAMCO, params=params, headers=headers, timeout=10)
        print_response("Testing getKamcoPbctCltrList (Kamco Auction)", r)
    except Exception as e:
        print(f"Kamco Test Failed: {e}")

if __name__ == "__main__":
    test_unify()
    test_kamco()
"""
        
        # Upload using SFTP to /tmp directly from string
        sftp = client.open_sftp()
        remote_diag = '/tmp/compare_services.py'
        print(f"Uploading embedded script -> {remote_diag}...")
        with sftp.open(remote_diag, 'w') as f:
            f.write(diag_code)
        sftp.close()
        
        if True: # Logic flow preservation
            # Docker cp
            container_path = "/tmp/compare_services.py"
            print(f"Copying {remote_diag} into container -> {container_path}...")
            cp_cmd = f"echo {PASS} | sudo -S docker cp {remote_diag} {target_container}:{container_path}"
            stdin, stdout, stderr = client.exec_command(cp_cmd)
            exit_code = stdout.channel.recv_exit_status()
            if exit_code != 0:
                print(f"Docker CP Failed: {stderr.read().decode()}")
            else:
                print("Docker CP Successful.")
            
            print("Executing script inside container...")
            # Check if file exists first
            check_cmd = f"echo {PASS} | sudo -S docker exec {target_container} ls -l {container_path}"
            stdin, stdout, stderr = client.exec_command(check_cmd)
            print(f"File check output:\n{stdout.read().decode()}\nStderr: {stderr.read().decode()}")
            
            run_cmd = f"echo {PASS} | sudo -S docker exec {target_container} sh -c 'python {container_path}'"
            stdin, stdout, stderr = client.exec_command(run_cmd)
            
            out = stdout.read().decode()
            err = stderr.read().decode()
            print(f"Container Python Result:\n{out}")
            if err:
                print(f"Container Stderr:\n{err}")
        
        client.close()
        
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    check_connectivity()
