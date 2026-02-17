import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_status():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        print("="*60)
        print("📊 Current Server Status (Split Deployment)")
        print("="*60)
        
        # Check running containers
        print("\n🐳 Running Containers:")
        stdin, stdout, stderr = client.exec_command(
            f'echo {PASS} | sudo -S docker ps --format "table {{{{.Names}}}}\t{{{{.Status}}}}\t{{{{.Ports}}}}" | grep -E "gundammap|NAMES"'
        )
        print(stdout.read().decode())
        
        # Test connection - Frontend
        print("\n🌐 Testing Frontend connection (Port 8004):")
        stdin, stdout, stderr = client.exec_command(
            'curl -I http://localhost:8004 2>&1 | head -5'
        )
        print(stdout.read().decode())

        # Test connection - Backend
        print("\n⚙️ Testing Backend connection (Port 8084):")
        stdin, stdout, stderr = client.exec_command(
            'curl -I http://localhost:8084 2>&1 | head -5'
        )
        print(stdout.read().decode())
        
        print("\n" + "="*60)
        print("✅ Status Check Complete!")
        print("="*60)
        print("\n📌 Frontend URL: http://175.126.187.59:8004")
        print("📌 Backend (API): http://175.126.187.59:8084")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_status()
