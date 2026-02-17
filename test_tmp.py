import paramiko
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def test_tmp_upload():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        sftp = client.open_sftp()
        
        # Try to upload a small dummy file to /tmp
        with sftp.open('/tmp/test_antigravity.txt', 'w') as f:
            f.write('test')
        print("Upload to /tmp successful")
        
        client.close()
    except Exception as e:
        print(f"Upload to /tmp failed: {e}")

if __name__ == "__main__":
    test_tmp_upload()
