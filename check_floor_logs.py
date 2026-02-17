import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

try:
    print("Connecting to server...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    # Get the container name
    cmd_check = f'echo {PASS} | sudo -S docker ps --format "{{{{.Names}}}}"'
    stdin, stdout, stderr = client.exec_command(cmd_check)
    running_containers = stdout.read().decode().splitlines()
    
    target_container = None
    for name in running_containers:
        if 'gundammap' in name and 'web' in name:
            target_container = name
            break
    
    if target_container:
        print(f"Found container: {target_container}")
        print("\nFetching logs (last 100 lines with Floor Debug)...")
        cmd_logs = f'echo {PASS} | sudo -S docker logs {target_container} 2>&1 | grep -i "Floor Debug" | tail -100'
        stdin, stdout, stderr = client.exec_command(cmd_logs)
        logs = stdout.read().decode()
        if logs:
            print(logs)
        else:
            print("No Floor Debug logs found yet. Showing last 50 lines of all logs:")
            cmd_logs_all = f'echo {PASS} | sudo -S docker logs {target_container} 2>&1 | tail -50'
            stdin, stdout, stderr = client.exec_command(cmd_logs_all)
            print(stdout.read().decode())
    else:
        print("Container not found")
    
    client.close()
except Exception as e:
    print(f"Error: {e}")
