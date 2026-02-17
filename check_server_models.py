import paramiko
import os
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')

def check_models():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"[*] Connecting to {HOST}...")
        client.connect(HOST, username=USER, password=PASS, timeout=10)
        print("[OK] Connected\n")
        
        # Check models.py on server
        print("="*60)
        print("[CHECK] Current models.py on server:")
        print("="*60)
        stdin, stdout, stderr = client.exec_command(
            f"echo {PASS} | sudo -S cat /volume1/docker/gundammap/maps/models.py"
        )
        output = stdout.read().decode('utf-8', errors='ignore')
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    check_models()
