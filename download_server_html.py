import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap/templates/maps/index.html'
LOCAL_PATH = 'index_from_server.html'

def download_remote_file():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    sftp = client.open_sftp()
    sftp.get(REMOTE_PATH, LOCAL_PATH)
    sftp.close()
    
    print(f"Downloaded {REMOTE_PATH} to {LOCAL_PATH}")
    
    client.close()

if __name__ == "__main__":
    download_remote_file()
