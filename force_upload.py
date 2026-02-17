import paramiko
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def force_upload():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        sftp = client.open_sftp()
        
        local_path = r'e:/Antigravity/Gundammap/templates/maps/index.html'
        remote_path = '/volume1/docker/gundammap/templates/maps/index.html'
        
        print(f"Uploading {local_path} to {remote_path}...")
        
        # Check if remote dir exists
        try:
             sftp.stat('/volume1/docker/gundammap/templates/maps')
        except FileNotFoundError:
             print("Remote directory not found, making needed dirs...")
             try: sftp.mkdir('/volume1/docker/gundammap/templates')
             except: pass
             try: sftp.mkdir('/volume1/docker/gundammap/templates/maps')
             except: pass
             
        sftp.put(local_path, remote_path)
        print("Force upload success.")
        client.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    force_upload()
