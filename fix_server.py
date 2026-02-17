import paramiko
import time

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def run_command(ssh, cmd, description, wait_time=2):
    """Run a command and print results"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(wait_time)
    
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    if output:
        print("✅ Output:")
        print(output)
    if error and "warning" not in error.lower():
        print("⚠️  Error/Warning:")
        print(error)
    
    return output, error

def fix_and_restart():
    try:
        print("🚀 Connecting to NAS server...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        print("✅ Connected successfully!\n")
        
        # 1. Stop all containers
        print("\n" + "🛑 STEP 1: Stopping all containers...")
        run_command(client,
                   f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose down',
                   "Stopping Docker Compose",
                   wait_time=5)
        
        # 2. Remove old containers (if any)
        print("\n" + "🗑️  STEP 2: Cleaning up old containers...")
        run_command(client,
                   f'echo {PASS} | sudo -S /usr/local/bin/docker ps -a --filter "name=gundammap" -q | xargs -r sudo /usr/local/bin/docker rm -f',
                   "Removing Old Containers",
                   wait_time=3)
        
        # 3. Rebuild containers
        print("\n" + "🔨 STEP 3: Rebuilding containers...")
        run_command(client,
                   f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose build --no-cache',
                   "Building Fresh Containers",
                   wait_time=30)
        
        # 4. Start containers
        print("\n" + "▶️  STEP 4: Starting containers...")
        run_command(client,
                   f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose up -d',
                   "Starting Docker Compose",
                   wait_time=10)
        
        # 5. Wait for containers to be ready
        print("\n⏳ Waiting 10 seconds for containers to initialize...")
        time.sleep(10)
        
        # 6. Run migrations
        print("\n" + "📊 STEP 5: Running database migrations...")
        output, _ = run_command(client,
                   f'echo {PASS} | sudo -S /usr/local/bin/docker ps --format "{{{{.Names}}}}" | grep web',
                   "Finding Web Container")
        
        if output.strip():
            container_name = output.strip().split('\n')[0]
            run_command(client,
                       f'echo {PASS} | sudo -S /usr/local/bin/docker exec {container_name} python manage.py migrate',
                       "Running Migrations",
                       wait_time=5)
            
            # 7. Collect static files
            print("\n" + "📦 STEP 6: Collecting static files...")
            run_command(client,
                       f'echo {PASS} | sudo -S /usr/local/bin/docker exec {container_name} python manage.py collectstatic --noinput',
                       "Collecting Static Files",
                       wait_time=3)
        
        # 8. Check final status
        print("\n" + "🔍 STEP 7: Checking final status...")
        run_command(client,
                   f'echo {PASS} | sudo -S /usr/local/bin/docker-compose ps',
                   "Container Status",
                   wait_time=2)
        
        # 9. Check logs
        if output.strip():
            print("\n" + "📋 STEP 8: Checking recent logs...")
            run_command(client,
                       f'echo {PASS} | sudo -S /usr/local/bin/docker logs --tail 30 {container_name}',
                       "Recent Logs",
                       wait_time=2)
        
        # 10. Test connection
        print("\n" + "🌐 STEP 9: Testing connection...")
        run_command(client,
                   'curl -I http://localhost:8000 2>&1 | head -10',
                   "Connection Test",
                   wait_time=2)
        
        print("\n" + "="*60)
        print("✅ Restart Complete!")
        print("="*60)
        print("\n📌 Next Steps:")
        print("1. Try accessing: http://175.126.187.59:8000")
        print("2. If still not working, check firewall settings on NAS")
        print("3. Ensure port 8000 is open in DSM Control Panel > Security > Firewall")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_and_restart()
