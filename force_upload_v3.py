import paramiko
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def force_upload_debug():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        sftp = client.open_sftp()
        
        # Verify local file
        local = r'e:/Antigravity/Gundammap/templates/maps/index.html'
        if not os.path.exists(local):
            print(f"Local file not found: {local}")
            return

        # Verify remote path components
        p = '/volume1/docker/gundammap/templates/maps'
        try:
            sftp.stat(p)
            print(f"Remote dir exists: {p}")
        except FileNotFoundError:
            print(f"Remote dir NOT found: {p}")

        # Upload
        print("Uploading...")
        sftp.put(local, p + '/index.html')
        print("Success!")
        client.close()
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    force_upload_debug()
