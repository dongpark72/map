import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

try:
    print("Connecting to server...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS, timeout=10)
    
    # Check Docker status
    cmd_check = f'echo {PASS} | sudo -S docker ps --format "{{{{.Names}}}}\t{{{{.Status}}}}"'
    stdin, stdout, stderr = client.exec_command(cmd_check)
    containers = stdout.read().decode()
    errors = stderr.read().decode()
    
    print("Docker containers:")
    print(containers)
    if errors:
        print(f"Errors: {errors}")
    
    # Check if web container is running
    if 'gundammap' in containers and 'web' in containers:
        # Get container name
        for line in containers.split('\n'):
            if 'gundammap' in line and 'web' in line:
                container_name = line.split('\t')[0]
                print(f"\nFound container: {container_name}")
                
                # Check logs for errors
                cmd_logs = f'echo {PASS} | sudo -S docker logs {container_name} --tail 50 2>&1'
                stdin, stdout, stderr = client.exec_command(cmd_logs)
                logs = stdout.read().decode()
                print(f"\nRecent logs:\n{logs[-2000:]}")
                break
    else:
        print("\n⚠️ Web container not found or not running!")
        print("\nTrying to restart...")
        cmd_restart = f'cd /volume1/docker/gundammap && echo {PASS} | sudo -S docker-compose restart web'
        stdin, stdout, stderr = client.exec_command(cmd_restart)
        print(stdout.read().decode())
        print(stderr.read().decode())
    
    client.close()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
