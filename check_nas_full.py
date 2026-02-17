import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_all():
    output = []
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        cmd = f"echo {PASS} | sudo -S docker ps -a"
        stdin, stdout, stderr = client.exec_command(cmd)
        output.append("--- All Containers ---")
        output.append(stdout.read().decode())
        
        # Try to find the actual container name for web
        cmd = f"echo {PASS} | sudo -S docker ps -a --filter name=web --format '{{{{.Names}}}}'"
        stdin, stdout, stderr = client.exec_command(cmd)
        web_container = stdout.read().decode().strip().split('\n')[0]
        
        if web_container:
            output.append(f"--- Logs for {web_container} ---")
            cmd = f"echo {PASS} | sudo -S docker logs {web_container} --tail 50"
            stdin, stdout, stderr = client.exec_command(cmd)
            output.append(stdout.read().decode())
            output.append(stderr.read().decode())
        else:
            output.append("Web container not found by name 'web'")
            
        client.close()
    except Exception as e:
        output.append(f"Error: {e}")
        
    with open('e:/Antigravity/Gundammap/nas_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

if __name__ == "__main__":
    check_all()
