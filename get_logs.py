import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def get_logs():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    docker_bin = "/usr/local/bin/docker"
    
    # 1. List all containers
    print("--- Docker PS -a ---")
    stdin, stdout, stderr = client.exec_command(f'echo {PASS} | sudo -S {docker_bin} ps -a --no-trunc')
    ps_output = stdout.read().decode()
    print(ps_output)
    
    # 2. Extract Container IDs
    lines = ps_output.strip().split('\n')
    if len(lines) > 1:
        # Skip header
        for line in lines[1:4]: # Check last few
            parts = line.split()
            cid = parts[0]
            name = parts[-1]
            print(f"\n--- Logs for {name} ({cid}) ---")
            
            stdin, stdout, stderr = client.exec_command(f'echo {PASS} | sudo -S {docker_bin} logs {cid}')
            print(stdout.read().decode())
            print(stderr.read().decode())
            
    client.close()

if __name__ == "__main__":
    get_logs()
