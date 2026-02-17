import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_status_debug():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        # Try simple command first
        cmd = f'echo {PASS} | sudo -S ls /'
        stdin, stdout, stderr = client.exec_command(cmd)
        print("--- LS ROOT ---")
        print(stdout.read().decode())
        print("STDERR:", stderr.read().decode())

        # Try docker
        # Try full path if known or just 'docker'
        cmd = f'echo {PASS} | sudo -S docker ps -a'
        stdin, stdout, stderr = client.exec_command(cmd)
        print("--- Docker PS ---")
        print(stdout.read().decode())
        print("STDERR:", stderr.read().decode())
        
        client.close()
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    check_status_debug()
