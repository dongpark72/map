import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def deep_restart():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        print("Deep restarting containers using 'docker compose'...")
        # Try both 'docker-compose' and 'docker compose'
        cmd = f"cd {REMOTE_PATH} && echo {PASS} | sudo -S docker compose down && echo {PASS} | sudo -S docker compose up -d"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        if "command not found" in out or "command not found" in err:
            print("Falling back to full path /usr/local/bin/docker-compose...")
            cmd = f"cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose down && echo {PASS} | sudo -S /usr/local/bin/docker-compose up -d"
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode()
            err = stderr.read().decode()

        print(out)
        print(err)
        print("Done.")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deep_restart()
