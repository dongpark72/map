import paramiko
from scp import SCPClient
import time

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def fix_database_issue():
    try:
        print("🚀 Connecting to NAS...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        print("✅ Connected!\n")
        
        # Upload updated .env file
        print("📤 Uploading updated .env file...")
        with SCPClient(client.get_transport()) as scp:
            scp.put('.env', f'{REMOTE_PATH}/.env')
        print("✅ .env file uploaded!\n")
        
        # Stop containers
        print("🛑 Stopping containers...")
        stdin, stdout, stderr = client.exec_command(
            f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose down'
        )
        time.sleep(3)
        print(stdout.read().decode())
        
        # Remove database volume to reset it
        print("🗑️  Removing old database volume...")
        stdin, stdout, stderr = client.exec_command(
            f'echo {PASS} | sudo -S /usr/local/bin/docker volume rm gundammap_postgres_data'
        )
        time.sleep(2)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(output)
        if error and "not found" not in error.lower():
            print("Note:", error)
        
        # Start containers
        print("\n▶️  Starting containers with fresh database...")
        stdin, stdout, stderr = client.exec_command(
            f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose up -d'
        )
        time.sleep(10)
        print(stdout.read().decode())
        
        # Wait for database to be ready
        print("\n⏳ Waiting for database to initialize (20 seconds)...")
        time.sleep(20)
        
        # Run migrations
        print("\n📊 Running database migrations...")
        stdin, stdout, stderr = client.exec_command(
            f'echo {PASS} | sudo -S /usr/local/bin/docker ps --format "{{{{.Names}}}}" | grep web'
        )
        container = stdout.read().decode().strip()
        
        if container:
            print(f"Container: {container}")
            stdin, stdout, stderr = client.exec_command(
                f'echo {PASS} | sudo -S /usr/local/bin/docker exec {container} python manage.py migrate'
            )
            time.sleep(5)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err:
                print("Migration output:", err)
        
        # Check status
        print("\n📊 Final Status:")
        stdin, stdout, stderr = client.exec_command(
            f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose ps'
        )
        print(stdout.read().decode())
        
        # Check logs
        print("\n📋 Recent logs:")
        if container:
            stdin, stdout, stderr = client.exec_command(
                f'echo {PASS} | sudo -S /usr/local/bin/docker logs --tail 20 {container}'
            )
            time.sleep(2)
            logs = stdout.read().decode()
            err_logs = stderr.read().decode()
            
            if logs:
                print("STDOUT:", logs)
            if err_logs:
                print("STDERR:", err_logs)
        
        # Test connection
        print("\n🌐 Testing connection...")
        stdin, stdout, stderr = client.exec_command(
            'curl -I http://localhost:8000 2>&1 | head -5'
        )
        print(stdout.read().decode())
        
        print("\n" + "="*70)
        print("✅ Fix Complete!")
        print("="*70)
        print("\n📌 Try accessing: http://175.126.187.59:8000")
        print("📌 If still not accessible, check NAS firewall settings")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_database_issue()
