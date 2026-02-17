import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_django_log():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        docker_bin = "/usr/local/bin/docker"
        
        # Get Web Container ID
        cmd = f'echo {PASS} | sudo -S {docker_bin} ps -q -f name=web'
        stdin, stdout, stderr = client.exec_command(cmd)
        cid = stdout.read().decode().strip()
        
        if cid:
            print(f"Checking logs for {cid}...")
            cmd = f'echo {PASS} | sudo -S {docker_bin} logs {cid}'
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode())
            print(stderr.read().decode())
        else:
            print("Web container not found running.")
            # Check stopped
            cmd = f'echo {PASS} | sudo -S {docker_bin} ps -a'
            stdin, stdout, stderr = client.exec_command(cmd)
            print("--- All Containers ---")
            print(stdout.read().decode())
            
        client.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check_django_log()
