import paramiko
import time

# Configuration
HOST = '175.126.187.59'
PORT = 22
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def run_server():
    print(f"Connecting to {HOST}...")
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, PORT, USER, PASS)
        print("Connected.")
        
        # Command to run
        # Synology container manager uses 'docker-compose' usually usually available in path or /usr/local/bin/docker-compose
        # We use 'sudo -S' to feed password to sudo
        
        cmds = [
            f'cd {REMOTE_PATH}',
            # Stop existing if any
            f'echo {PASS} | sudo -S docker-compose down', 
            # Build and Up
            f'echo {PASS} | sudo -S docker-compose up -d --build'
        ]
        
        full_cmd = ' && '.join(cmds)
        print("Executing Docker Compose commands...")
        
        stdin, stdout, stderr = client.exec_command(full_cmd)
        
        # Stream output
        while True:
            line = stdout.readline()
            if not line:
                break
            print(line.strip())
            
        err = stderr.read().decode()
        if err:
            # sudo -S writes prompt to stderr, so ignore that, but print others
            if "password" not in err.lower(): 
                print(f"STDERR: {err}")
            else:
                # If there is real error mixed with password prompt
                lines = err.split('\n')
                for l in lines:
                    if "password" not in l.lower() and l.strip():
                        print(f"STDERR: {l.strip()}")

        print("Finished.")
        client.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_server()
