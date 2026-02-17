import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap/templates/maps/index.html'

def check_remote_file():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    # Check if realprice-panel exists in remote file
    cmd = f"grep -c 'realprice-panel' {REMOTE_PATH} || echo '0'"
    stdin, stdout, stderr = client.exec_command(cmd)
    count = stdout.read().decode().strip()
    
    print(f"Remote file realprice-panel occurrences: {count}")
    
    # Check version
    cmd = f"grep 'v1\\.' {REMOTE_PATH} | head -1"
    stdin, stdout, stderr = client.exec_command(cmd)
    version = stdout.read().decode().strip()
    
    print(f"Remote file version line: {version}")
    
    # Check for real price button
    cmd = f"grep -c 'real-btn\\|실' {REMOTE_PATH} || echo '0'"
    stdin, stdout, stderr = client.exec_command(cmd)
    btn_count = stdout.read().decode().strip()
    
    print(f"Real price button occurrences: {btn_count}")
    
    client.close()

if __name__ == "__main__":
    check_remote_file()
