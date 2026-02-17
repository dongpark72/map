import paramiko
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def force_upload_absolute():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        sftp = client.open_sftp()
        
        # Absolute path issues?
        # Try changing directory first
        sftp.chdir('/volume1/docker/gundammap')
        print("CWD changed to root")
        sftp.chdir('templates')
        print("CWD changed to templates")
        sftp.chdir('maps')
        print("CWD changed to maps")
        
        local = r'e:/Antigravity/Gundammap/templates/maps/index.html'
        sftp.put(local, 'index.html')
        print("Success via relative path!")
        
        client.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    force_upload_absolute()
