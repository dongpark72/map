import paramiko
import os
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')

def run_ssh_command(client, command, description):
    print(f"\n{'='*60}")
    print(f"[CHECK] {description}")
    print(f"{'='*60}")
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    
    if output:
        print(output)
    if error and "sudo" not in error.lower():
        print(f"[WARNING] Error: {error}")
    return output, error

def diagnose():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"[*] Connecting to {HOST}...")
        client.connect(HOST, username=USER, password=PASS, timeout=10)
        print("[OK] SSH connection established\n")
        
        # Check Docker container status
        run_ssh_command(client, 
            f"echo {PASS} | sudo -S docker ps -a | grep gundammap",
            "Docker Container Status")
        
        # Check web container logs (last 100 lines)
        run_ssh_command(client, 
            f"echo {PASS} | sudo -S docker logs --tail 100 gundammap_web_1 2>&1",
            "Web Container Logs (Last 100 lines)")
        
        # Check if port 8000 is listening inside container
        run_ssh_command(client,
            f"echo {PASS} | sudo -S docker exec gundammap_web_1 netstat -tuln 2>&1 || echo {PASS} | sudo -S docker exec gundammap_web_1 ss -tuln 2>&1",
            "Port Listening Status Inside Container")
        
        # Check container processes
        run_ssh_command(client,
            f"echo {PASS} | sudo -S docker exec gundammap_web_1 ps aux 2>&1",
            "Processes Running Inside Container")
        
        # Check Django settings
        run_ssh_command(client,
            f"echo {PASS} | sudo -S docker exec gundammap_web_1 cat /app/gundammap/settings.py 2>&1 | grep -A 5 'ALLOWED_HOSTS'",
            "Django ALLOWED_HOSTS Configuration")
        
        # Try to restart the web container
        print(f"\n{'='*60}")
        print("[*] Attempting to restart web container...")
        print(f"{'='*60}")
        run_ssh_command(client,
            f"echo {PASS} | sudo -S docker restart gundammap_web_1",
            "Restarting Web Container")
        
        # Wait a moment and check logs again
        import time
        print("\n[*] Waiting 5 seconds for container to start...")
        time.sleep(5)
        
        run_ssh_command(client,
            f"echo {PASS} | sudo -S docker logs --tail 50 gundammap_web_1 2>&1",
            "Web Container Logs After Restart")
        
        client.close()
        print("\n[OK] Diagnostic complete!")
        
    except Exception as e:
        print(f"\n[ERROR] Error during diagnosis: {e}")

if __name__ == "__main__":
    diagnose()
