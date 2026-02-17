import paramiko
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def force_upload_final():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        sftp = client.open_sftp()
        
        local = r'e:/Antigravity/Gundammap/templates/maps/index.html'
        
        # We know /volume1/docker/gundammap/templates/maps exists from 'ls' command earlier.
        # But SFTP is acting weird with absolute paths or permission?
        # Let's try to upload to home and move it.
        
        print("Uploading to home...")
        sftp.put(local, 'index.html_temp')
        
        print("Moving to target...")
        cmd = f'echo {PASS} | sudo -S mv /volume1/homes/{USER}/index.html_temp /volume1/docker/gundammap/templates/maps/index.html'
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("Done.")
        client.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    force_upload_final()
