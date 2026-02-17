
import paramiko
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def get_latest_logs():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        # Get the container name
        stdin, stdout, stderr = client.exec_command("echo " + PASS + " | sudo -S docker ps --format '{{.Names}}'")
        containers = stdout.read().decode().strip().split('\n')
        target = next((c for c in containers if 'gundammap' in c and 'web' in c), None)
        
        if target:
            print(f"Fetching logs for {target}...")
            # Get last 100 lines of logs
            stdin, stdout, stderr = client.exec_command(f"echo {PASS} | sudo -S docker logs --tail 100 {target}")
            print(stdout.read().decode())
            print(stderr.read().decode())
        else:
            print("Container not found.")
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_latest_logs()
