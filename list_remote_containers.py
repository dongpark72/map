import paramiko
import os
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')

def check_containers():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {HOST}...")
        client.connect(HOST, username=USER, password=PASS, timeout=10)
        
        cmd = f"echo {PASS} | sudo -S docker ps --format '{{{{.Names}}}}'"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("\nRunning Containers:")
        print(stdout.read().decode('utf-8'))
        
        error = stderr.read().decode('utf-8')
        if error:
            print(f"Error: {error}")
            
        client.close()
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_containers()
