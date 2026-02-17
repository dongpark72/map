import paramiko
import os
import base64

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap/gundammap/settings.py'
LOCAL_PATH = 'e:/Antigravity/Gundammap/gundammap/settings.py'

def force_upload():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        with open(LOCAL_PATH, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode('utf-8')
            
        full_cmd = f"echo {PASS} | sudo -S bash -c \"echo '{content_b64}' | base64 -d > '{REMOTE_PATH}'\""
        stdin, stdout, stderr = client.exec_command(full_cmd)
        
        print(stdout.read().decode())
        print(stderr.read().decode())
        print("Settings.py uploaded.")
        
        # Restart web
        cmd = f"echo {PASS} | sudo -S docker restart gundammap_web_1"
        client.exec_command(cmd)
        print("Web container restarted.")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_upload()
