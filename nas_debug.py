import paramiko
import time

# Configuration
HOST = '175.126.187.59'
PORT = 22
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def run_debug_build():
    print(f"Connecting to {HOST}...")
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, PORT, USER, PASS)
        print("Connected.")
        
        # Try a simpler build command and capture ALL output to see why it fails
        # Use no-cache to force build logs
        # And ensure we see the output immediately
        cmd = f'cd {REMOTE_PATH} && echo {PASS} | sudo -S docker-compose build --no-cache'
        
        print("Executing Docker Build (Debug Mode)...")
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True) 
        # get_pty=True helps with buffering and sudo interaction sometimes
        
        while True:
            line = stdout.readline()
            if not line: break
            print(line.strip())
            
        print("Done reading output.")
        client.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_debug_build()
