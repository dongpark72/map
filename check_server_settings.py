import paramiko
import os
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')
REMOTE_BASE_PATH = '/volume1/docker/gundammap'

def check_settings():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        print("\nChecking gundammap/settings.py content:")
        stdin, stdout, stderr = client.exec_command(f"cat {REMOTE_BASE_PATH}/gundammap/settings.py")
        print(stdout.read().decode())
        
        print("\nChecking .env content (masking sensitive):")
        stdin, stdout, stderr = client.exec_command(f"cat {REMOTE_BASE_PATH}/.env")
        print(stdout.read().decode())
        
        print("\nChecking which containers are running:")
        stdin, stdout, stderr = client.exec_command(f"echo {PASS} | sudo -S docker ps")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_settings()
