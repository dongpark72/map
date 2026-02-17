import paramiko
import time

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def run_command(ssh, cmd, description):
    """Run a command and print results"""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    if output:
        print("Output:")
        print(output)
    if error:
        print("Error:")
        print(error)
    
    return output, error

def diagnose():
    try:
        print("🚀 Connecting to NAS server...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        print("✅ Connected successfully!\n")
        
        # 1. Check Docker service status
        run_command(client, 
                   f'echo {PASS} | sudo -S systemctl status docker | head -20',
                   "Docker Service Status")
        
        # 2. Check if containers are running
        run_command(client,
                   f'echo {PASS} | sudo -S /usr/local/bin/docker ps -a',
                   "All Docker Containers")
        
        # 3. Check specific gundammap containers
        run_command(client,
                   f'echo {PASS} | sudo -S /usr/local/bin/docker ps --filter "name=gundammap"',
                   "Gundammap Containers")
        
        # 4. Check port bindings
        run_command(client,
                   f'echo {PASS} | sudo -S /usr/local/bin/docker ps --format "table {{{{.Names}}}}\t{{{{.Ports}}}}"',
                   "Container Port Bindings")
        
        # 5. Check if port 8000 is listening
        run_command(client,
                   f'echo {PASS} | sudo -S netstat -tlnp | grep 8000',
                   "Port 8000 Status")
        
        # 6. Check docker-compose status
        run_command(client,
                   f'cd /volume1/docker/gundammap && echo {PASS} | sudo -S /usr/local/bin/docker-compose ps',
                   "Docker Compose Status")
        
        # 7. Check web container logs (last 50 lines)
        output, _ = run_command(client,
                   f'echo {PASS} | sudo -S /usr/local/bin/docker ps --format "{{{{.Names}}}}" | grep web',
                   "Finding Web Container")
        
        if output.strip():
            container_name = output.strip().split('\n')[0]
            run_command(client,
                       f'echo {PASS} | sudo -S /usr/local/bin/docker logs --tail 50 {container_name}',
                       f"Web Container Logs ({container_name})")
        
        # 8. Check if files exist
        run_command(client,
                   'ls -la /volume1/docker/gundammap/',
                   "Project Files")
        
        # 9. Check .env file
        run_command(client,
                   'cat /volume1/docker/gundammap/.env',
                   "Environment Variables")
        
        # 10. Test connection to localhost:8000 from inside the server
        run_command(client,
                   'curl -I http://localhost:8000 2>&1',
                   "Test Local Connection to Port 8000")
        
        # 11. Check firewall rules
        run_command(client,
                   f'echo {PASS} | sudo -S iptables -L -n | grep 8000',
                   "Firewall Rules for Port 8000")
        
        print("\n" + "="*60)
        print("✅ Diagnosis Complete!")
        print("="*60)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose()
