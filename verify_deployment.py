import paramiko
import os
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')
REMOTE_PATH = '/volume1/docker/gundammap/templates/maps/map_app.html'

def verify_remote_content():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {HOST}...")
        client.connect(HOST, username=USER, password=PASS, timeout=10)
        
        # Check for the specific comment unique to our new version
        cmd = f"echo {PASS} | sudo -S grep 'Removed to ensure 100% scale' '{REMOTE_PATH}'"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        output = stdout.read().decode('utf-8')
        
        print("\nVerification Result:")
        if output.strip():
            print("SUCCESS: Found the updated code comment on the server.")
            print(f"Match: {output.strip()}")
        else:
            print("FAILURE: Could not find the updated code on the server.")
            
        client.close()
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    verify_remote_content()
