import paramiko
import os
import hashlib
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')
REMOTE_BASE_PATH = '/volume1/docker/gundammap'

FILES_TO_CHECK = [
    'maps/views.py',
    'maps/urls.py',
    'templates/maps/map_app.html'
]

def get_remote_file_info(client, remote_path):
    cmd = f"ls -l '{remote_path}'"
    stdin, stdout, stderr = client.exec_command(cmd)
    output = stdout.read().decode().strip()
    if output:
        # returns something like: -rwxrwxrwx 1 root root 149915 Jan 11 01:10 /volume1/docker/gundammap/templates/maps/map_app.html
        parts = output.split()
        if len(parts) >= 5:
            return int(parts[4]) # size is usually the 5th field in ls -l
    return -1

def verify_deployment():
    print("=== Checking Server Deployment Status ===")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)

        all_match = True
        
        for rel_path in FILES_TO_CHECK:
            local_path = os.path.join(LOCAL_BASE_PATH, rel_path)
            remote_path = os.path.join(REMOTE_BASE_PATH, rel_path).replace('\\', '/')
            
            if not os.path.exists(local_path):
                print(f"[SKIP] Local file not found: {rel_path}")
                continue
                
            local_size = os.path.getsize(local_path)
            remote_size = get_remote_file_info(client, remote_path)
            
            if remote_size == local_size:
                print(f"[MATCH] {rel_path}: Size matches ({local_size} bytes)")
            else:
                print(f"[MISMATCH] {rel_path}: Local={local_size} vs Remote={remote_size}")
                all_match = False
                
        # Check container uptime
        print("\n=== Docker Container Status ===")
        stdin, stdout, stderr = client.exec_command("echo " + PASS + " | sudo -S docker ps --format '{{.Names}}: {{.Status}}' | grep gundammap")
        print(stdout.read().decode().strip())

        client.close()
        
        if all_match:
            print("\n✅ Verification Successful: Critical files size match.")
        else:
            print("\n❌ Verification Failed: Some files do not match.")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    verify_deployment()
