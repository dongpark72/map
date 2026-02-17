import paramiko
import time

HOST = '175.126.187.59'
PORT = 22
USER = 'dongpark72'
PASS = 'timess9746'

def diagnose():
    print("=" * 60)
    print("🚑 Server Diagnosis")
    print("=" * 60)
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, PORT, USER, PASS, timeout=10)
        print("✅ SSH Connected")
        
        # 1. Check Container Status
        print("\n🐳 Checking Container Status:")
        cmd = f'echo {PASS} | sudo -S docker ps -a --filter name=gundammap_web_1'
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        
        # 2. Check Logs (last 50 lines) to see if it crashed
        print("\n📋 Checking Recent Logs:")
        cmd = f'echo {PASS} | sudo -S docker logs --tail 50 gundammap_web_1 2>&1'
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        
        client.close()
        
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    diagnose()
