import paramiko
from scp import SCPClient
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'
LOCAL_PATH = os.getcwd()

def upload_and_restart():
    try:
        print("🚀 Connecting to NAS...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        print("✅ Connected!\n")
        
        # Upload updated docker-compose.yml
        print("📤 Uploading docker-compose.yml...")
        with SCPClient(client.get_transport()) as scp:
            scp.put('docker-compose.yml', f'{REMOTE_PATH}/docker-compose.yml')
        print("✅ Uploaded!\n")
        
        # Restart containers
        print("🔄 Restarting containers...")
        stdin, stdout, stderr = client.exec_command(
            f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose down'
        )
        print(stdout.read().decode())
        
        stdin, stdout, stderr = client.exec_command(
            f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose up -d'
        )
        print(stdout.read().decode())
        
        print("\n⏳ Waiting for containers to start...")
        import time
        time.sleep(10)
        
        # Check status
        print("\n📊 Container Status:")
        stdin, stdout, stderr = client.exec_command(
            f'echo {PASS} | sudo -S /usr/local/bin/docker-compose ps'
        )
        print(stdout.read().decode())
        
        print("\n✅ Done!")
        print("📌 Try accessing: http://175.126.187.59:8000")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_and_restart()
