import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_final_status():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        docker_bin = "/usr/local/bin/docker"
        
        # Check containers
        cmd = f'echo {PASS} | sudo -S {docker_bin} ps'
        stdin, stdout, stderr = client.exec_command(cmd)
        print("--- Docker PS ---")
        out = stdout.read().decode()
        if not out.strip():
            print("(No running containers)")
        else:
            print(out)
            
        # Check all
        if not out.strip():
            cmd = f'echo {PASS} | sudo -S {docker_bin} ps -a'
            stdin, stdout, stderr = client.exec_command(cmd)
            print("--- Docker PS -a ---")
            print(stdout.read().decode())
            
        client.close()
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    check_final_status()
