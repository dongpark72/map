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
        print(f"Found container: {target_container}\n")
        
        # Get all logs and save to file
        print("Fetching all recent logs...")
        cmd_logs_all = f'echo {PASS} | sudo -S docker logs {target_container} 2>&1 | tail -200'
        stdin, stdout, stderr = client.exec_command(cmd_logs_all)
        all_logs = stdout.read().decode()
        
        # Save to file
        with open('server_logs.txt', 'w', encoding='utf-8') as f:
            f.write(all_logs)
        
        print("Logs saved to server_logs.txt")
        
        # Also print Floor Debug lines if any
        floor_lines = [line for line in all_logs.split('\n') if 'Floor Debug' in line]
        if floor_lines:
            print(f"\n\nFound {len(floor_lines)} Floor Debug lines:")
            print("=" * 80)
            for line in floor_lines:
                print(line)
        else:
            print("\n\nNo Floor Debug logs found. Showing last 30 lines:")
            print("=" * 80)
            print('\n'.join(all_logs.split('\n')[-30:]))
    else:
        print("Container not found")
    
    client.close()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
