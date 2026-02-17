import paramiko
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def test_sftp():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        print("Connected.")
        
        sftp = client.open_sftp()
        print("SFTP opened.")
        
        # List root to see where we are
        print(f"Current dir: {sftp.getcwd()}")
        print(f"Listing /: {sftp.listdir('/')}")
        print(f"Listing /tmp: {sftp.listdir('/tmp') if '/tmp' in sftp.listdir('/') else 'no /tmp'}")
        
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_sftp()
