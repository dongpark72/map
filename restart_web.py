import paramiko
import os
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')

def restart_web():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {HOST}...")
        client.connect(HOST, username=USER, password=PASS, timeout=10)
        
        print("Restarting 'gundam-web'...")
        cmd = f"echo {PASS} | sudo -S docker restart gundam-web"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Wait for finish
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print("Successfully restarted gundam-web")
        else:
            print("Failed to restart gundam-web")
            print(stderr.read().decode('utf-8'))
            
        client.close()
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    restart_web()
