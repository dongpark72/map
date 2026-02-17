
import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def tail_logs():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    stdin, stdout, stderr = client.exec_command(f"echo {PASS} | sudo -S docker ps --format '{{.Names}}'")
    containers = stdout.read().decode().strip().split('\n')
    target = next((c for c in containers if 'gundammap' in c and 'web' in c), None)
    
    if target:
        cmd = f"echo {PASS} | sudo -S docker logs --tail 50 {target}"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
    
    client.close()

if __name__ == "__main__":
    tail_logs()
