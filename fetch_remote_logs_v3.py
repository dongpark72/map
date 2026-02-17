import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def get_logs():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    print("Checking for all containers...")
    stdin, stdout, stderr = client.exec_command('sudo docker ps -a --format "{{.Names}}"')
    stdin.write(PASS + '\n')
    stdin.flush()
    containers = stdout.read().decode().strip().split('\n')
    print(f"All containers: {containers}")
    
    for container in containers:
        if 'gundammap' in container and 'web' in container:
            print(f"Fetching logs for {container}...")
            stdin, stdout, stderr = client.exec_command(f'sudo docker logs --tail 50 {container}')
            stdin.write(PASS + '\n')
            stdin.flush()
            print("STDOUT:", stdout.read().decode())
            print("STDERR:", stderr.read().decode())
            
    client.close()

if __name__ == "__main__":
    get_logs()
