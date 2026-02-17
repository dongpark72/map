import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_env():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        # Check environment variables seen by Docker
        cmd = f"echo {PASS} | sudo -S docker inspect gundammap_web_1 --format '{{{{range .Config.Env}}}}{{{{.}}}}{{{{println}}}}{{{{end}}}}'"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("--- Docker Container Env Variables ---")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_env()
