import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def get_logs():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    # Try common container names
    for name in ['gundammap-web-1', 'gundammap_web_1']:
        print(f"Trying logs for {name}...")
        cmd = f"echo {PASS} | sudo -S docker logs --tail 100 {name}"
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode()
        err = stderr.read().decode()
        if out or err:
            print(f"--- {name} STDOUT ---")
            print(out)
            print(f"--- {name} STDERR ---")
            print(err)
            
    client.close()

if __name__ == "__main__":
    get_logs()
