import paramiko
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def force_upload_corrected():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        sftp = client.open_sftp()
        
        local_path = r'e:/Antigravity/Gundammap/templates/maps/index.html'
        # Based on LS output, it seems structure exists but maybe I was mistyping or permission issue?
        # LS output showed: /volume1/docker/gundammap/templates/maps -> index.html exists.
        
        remote_path = '/volume1/docker/gundammap/templates/maps/index.html'
        
        print(f"Uploading {local_path} to {remote_path}...")
        sftp.put(local_path, remote_path)
        print("Force upload success.")
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_upload_corrected()
