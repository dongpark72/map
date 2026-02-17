import paramiko
import sys

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def run_foreground():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        docker_bin = "/usr/local/bin/docker"
        dc_bin = "/usr/local/bin/docker-compose"
        
        # Build first with logs
        print("--- Building ---")
        cmd = f'cd {REMOTE_PATH} && echo {PASS} | sudo -S {dc_bin} build'
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Stream output
        while True:
            line = stdout.readline()
            if not line: break
            print(line.strip())
        print(stderr.read().decode())
        
        if stdout.channel.recv_exit_status() != 0:
            print("Build failed!")
            return

        # Up
        print("--- Starting (Foreground) ---")
        # Run DB detached
        client.exec_command(f'cd {REMOTE_PATH} && echo {PASS} | sudo -S {dc_bin} up -d db')
        time.sleep(5)
        
        # Run Web foreground
        cmd = f'cd {REMOTE_PATH} && echo {PASS} | sudo -S {dc_bin} run --rm --service-ports web'
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        
        # Capture for 10 seconds then close? No, wait for error.
        import time
        start = time.time()
        while time.time() - start < 15:
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode())
            if stderr.channel.recv_ready():
                print(stderr.channel.recv(1024).decode())
            time.sleep(0.1)
            
        client.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    run_foreground()
