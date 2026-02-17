import paramiko
import time

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def get_logs_debug():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        docker_bin = "/usr/local/bin/docker"

        # Check stopped containers
        print("--- Docker PS -a ---")
        cmd = f'echo {PASS} | sudo -S {docker_bin} ps -a'
        stdin, stdout, stderr = client.exec_command(cmd)
        ps_out = stdout.read().decode()
        print(ps_out)
        
        # Parse output properly
        ids = []
        for line in ps_out.splitlines()[1:]:
            parts = line.split()
            if parts:
                ids.append(parts[0]) # Container ID
        
        for i in ids[:2]: # Check last 2
            print(f"--- Logs for {i} ---")
            cmd = f'echo {PASS} | sudo -S {docker_bin} logs {i}'
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode())
            print(stderr.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_logs_debug()
