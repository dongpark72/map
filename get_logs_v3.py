import paramiko
import time

HOST = '175.126.187.59'
PORT = 22
USER = 'dongpark72'
PASS = 'timess9746'

def get_logs():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, PORT, USER, PASS)
        print("Connected to server.")
        
        # Get logs from web container
        stdin, stdout, stderr = client.exec_command(f'echo {PASS} | sudo -S docker logs --tail 100 gundammap_web_1')
        print("Logs from gundammap_web_1:")
        print(stdout.read().decode())
        print("Errors (if any):")
        print(stderr.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    get_logs()
