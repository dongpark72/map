import paramiko
import time

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def restart_containers():
    try:
        print("🚀 Connecting to NAS...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        print("✅ Connected!\n")
        
        # Restart containers
        print("🔄 Restarting containers...")
        stdin, stdout, stderr = client.exec_command(
            f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose restart'
        )
        time.sleep(15)
        print(stdout.read().decode())
        
        # Wait for services to be ready
        print("\n⏳ Waiting 30 seconds for services to be ready...")
        time.sleep(30)
        
        # Check status
        print("\n📊 Container Status:")
        stdin, stdout, stderr = client.exec_command(
            f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose ps'
        )
        print(stdout.read().decode())
        
        # Check web logs
        print("\n📋 Web Container Logs:")
        stdin, stdout, stderr = client.exec_command(
            f'echo {PASS} | sudo -S /usr/local/bin/docker logs --tail 30 gundammap_web_1 2>&1'
        )
        print(stdout.read().decode())
        
        # Test connection
        print("\n🌐 Testing Connection:")
        stdin, stdout, stderr = client.exec_command(
            'curl -v http://localhost:8000 2>&1 | head -20'
        )
        result = stdout.read().decode()
        print(result)
        
        if "200 OK" in result or "HTTP" in result:
            print("\n✅ SUCCESS! Server is responding!")
        else:
            print("\n⚠️  Server may not be fully ready yet")
        
        print("\n" + "="*70)
        print("📌 Access URL: http://175.126.187.59:8000")
        print("="*70)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    restart_containers()
