import paramiko
from scp import SCPClient
import time
import os

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def repair_server():
    try:
        print("[Start] Connecting to NAS...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        print("[OK] Connected!\n")
        
        # 1. Upload modified settings.py
        print("[Upload] Uploading updated settings.py...")
        local_settings = os.path.join("gundammap", "settings.py")
        remote_settings = f"{REMOTE_PATH}/gundammap/settings.py"
        
        with SCPClient(client.get_transport()) as scp:
            scp.put(local_settings, remote_settings)
        print("[OK] settings.py uploaded!\n")
        
        # 2. Update .env on server to enable Postgres
        print("[Config] Updating .env to enable Postgres...")
        # Check current .env content
        stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_PATH}/.env')
        current_env = stdout.read().decode()
        
        if "USE_POSTGRES=True" not in current_env:
            print("  - Adding USE_POSTGRES=True to .env")
            cmd = f'echo "\nUSE_POSTGRES=True" >> {REMOTE_PATH}/.env'
            client.exec_command(cmd)
        else:
            print("  - USE_POSTGRES is already set.")
            
        # Verify
        stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_PATH}/.env')
        new_env = stdout.read().decode()
        if "USE_POSTGRES=True" not in new_env:
            print("[Warning] Failed to update .env via echo. Trying to re-upload local .env with modification.")
            # Read local .env
            env_content = ""
            if os.path.exists(".env"):
                with open(".env", "r") as f:
                    env_content = f.read()
            
            if "USE_POSTGRES" not in env_content:
                env_content += "\nUSE_POSTGRES=True\n"
            
            with open(".env.tmp", "w") as f:
                f.write(env_content)
            
            with SCPClient(client.get_transport()) as scp:
                scp.put(".env.tmp", f"{REMOTE_PATH}/.env")
            
            os.remove(".env.tmp")
            print("[OK] .env uploaded forcedly.")
            
        print("[OK] .env check complete!\n")

        # 3. Restart Containers
        print("[Restart] Restarting containers to apply changes...")
        # restart web container
        stdin, stdout, stderr = client.exec_command(
            f'cd {REMOTE_PATH} && echo {PASS} | sudo -S /usr/local/bin/docker-compose restart web'
        )
        print(stdout.read().decode())
        time.sleep(5)
        
        # 4. Migrate Database (Postgres)
        print("[Migrate] Running database migrations (Postgres)...")
        stdin, stdout, stderr = client.exec_command(
            f'echo {PASS} | sudo -S /usr/local/bin/docker ps --format "{{{{.Names}}}}" | grep web'
        )
        container = stdout.read().decode().strip()
        
        if container:
            print(f"Container: {container}")
            stdin, stdout, stderr = client.exec_command(
                f'echo {PASS} | sudo -S /usr/local/bin/docker exec {container} python manage.py migrate'
            )
            out = stdout.read().decode()
            err = stderr.read().decode()
            print(out)
            if err:
                print("Migration Error/Warning:", err)
        else:
            print("[Error] Web container not found!")
            return

        # 5. Check Logs
        print("\n[Logs] Checking logs...")
        stdin, stdout, stderr = client.exec_command(
             f'echo {PASS} | sudo -S /usr/local/bin/docker logs --tail 20 {container}'
        )
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # 6. Test Connection
        print("\n[Test] Testing connection...")
        stdin, stdout, stderr = client.exec_command(
            'curl -I http://localhost:8000 2>&1 | head -5'
        )
        print(stdout.read().decode())

        print("\n[Done] Repair Complete!")
        print("Please check http://175.126.187.59:8000")

    except Exception as e:
        print(f"[Error] Error: {e}")
        import traceback
        traceback.print_exc()
        
if __name__ == "__main__":
    repair_server()
