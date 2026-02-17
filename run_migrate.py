import paramiko
import time

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def run_migrate():
    try:
        print("🚀 Connecting to NAS...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        print("✅ Connected!\n")
        
        # Run migrate
        print("🔄 Running migrations...")
        stdin, stdout, stderr = client.exec_command(
            f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose exec -T web python manage.py migrate'
        )
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        client.close()
        print("✅ Done!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_migrate()
