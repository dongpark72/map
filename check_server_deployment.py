import paramiko
import os
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')
REMOTE_BASE_PATH = '/volume1/docker/gundammap'

def check_server_dir():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        print(f"Listing directory {REMOTE_BASE_PATH}:")
        stdin, stdout, stderr = client.exec_command(f"ls -R {REMOTE_BASE_PATH}")
        print(stdout.read().decode())
        
        print("\nChecking maps/urls.py content:")
        stdin, stdout, stderr = client.exec_command(f"cat {REMOTE_BASE_PATH}/maps/urls.py")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_server_dir()
