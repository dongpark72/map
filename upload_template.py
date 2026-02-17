import paramiko
from scp import SCPClient
import os
import sys

# Configuration
HOST = '175.126.187.59'
PORT = 22
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap/templates/maps'

def upload_template():
    print(f"Connecting to {HOST}...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, PORT, USER, PASS)
        print("Connected.")
        
        # Upload index.html
        local_file = os.path.join(os.getcwd(), 'templates', 'maps', 'index.html')
        remote_file = f'{REMOTE_PATH}/index.html'
        
        print(f"Uploading {local_file} -> {remote_file}")
        
        with SCPClient(client.get_transport()) as scp:
            scp.put(local_file, remote_file)
            
        print("Upload complete!")
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    upload_template()
