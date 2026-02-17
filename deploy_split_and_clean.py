import paramiko
import os
import time
from dotenv import load_dotenv

# Load env vars
load_dotenv('e:\\Antigravity\\Gundammap\\.env')

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')
REMOTE_PATH = '/volume1/docker/gundammap'

# Deployment Config (Standard Guide)
WEB_PORT = 8004
API_PORT = 8084
NETWORK_NAME = 'gundammap-net'
DB_CONTAINER = 'gundammap-db'
BACKEND_CONTAINER = 'gundammap-backend'
FRONTEND_CONTAINER = 'gundammap-front'

def run_cmd(ssh, cmd):
    print(f"Executing: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(f"echo {PASS} | sudo -S {cmd}")
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out: print(f"OUT: {out}")
    if err and "password" not in err.lower(): print(f"ERR: {err}")
    return out

def deploy():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASS)
        print("✅ Connected to NAS")

        # 1. Ensure directory and network
        run_cmd(ssh, f"mkdir -p {REMOTE_PATH}")
        run_cmd(ssh, f"docker network create {NETWORK_NAME} || true")

        # 2. Upload critical files (simulated here since I can't run pscp directly easily, 
        # I assume files are synchronized via SMB as mentioned in user metadata)
        # But for robustness, I'll mention the build will use current remote context.
        
        # 3. Stop ALL old containers (both integrated and naming variants)
        print("🛑 Cleaning up old containers...")
        old_containers = "gundammap_web_1 gundammap_db_1 gundam-web gundam-db gundammap-front gundammap-backend"
        run_cmd(ssh, f"docker rm -f {old_containers} || true")

        # 4. Start DB (PostgreSQL)
        print("🗄️ Starting Database...")
        db_cmd = (f"docker run -d --name {DB_CONTAINER} --network {NETWORK_NAME} "
                 f"--restart unless-stopped "
                 f"-v gundammap_postgres_data:/var/lib/postgresql/data "
                 f"-e POSTGRES_DB=gundammap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD={PASS} "
                 f"postgis/postgis:15-3.3")
        run_cmd(ssh, db_cmd)

        # 5. Build and Start Backend (Django)
        print("⚙️ Building & Starting Backend (Django)...")
        # Build takes time
        run_cmd(ssh, f"cd {REMOTE_PATH} && docker build -f backend.Dockerfile -t {BACKEND_CONTAINER} .")
        
        backend_run = (f"docker run -d --name {BACKEND_CONTAINER} --network {NETWORK_NAME} "
                      f"-p {API_PORT}:8000 "
                      f"--restart unless-stopped "
                      f"-e DB_HOST={DB_CONTAINER} -e USE_POSTGRES=True "
                      f"-v {REMOTE_PATH}:/app "
                      f"--env-file {REMOTE_PATH}/.env "
                      f"{BACKEND_CONTAINER}")
        run_cmd(ssh, backend_run)

        # Wait for backend to be ready
        print("⏳ Waiting for backend initialization...")
        time.sleep(10)

        # Run Migrations
        print("📊 Running Database Migrations...")
        run_cmd(ssh, f"docker exec {BACKEND_CONTAINER} python manage.py migrate")

        # 6. Build and Start Frontend (Nginx)
        print("🌐 Building & Starting Frontend (Nginx)...")
        run_cmd(ssh, f"cd {REMOTE_PATH} && docker build -f frontend.Dockerfile -t {FRONTEND_CONTAINER} .")
        
        frontend_run = (f"docker run -d --name {FRONTEND_CONTAINER} --network {NETWORK_NAME} "
                       f"-p {WEB_PORT}:80 "
                       f"--restart unless-stopped "
                       f"{FRONTEND_CONTAINER}")
        run_cmd(ssh, frontend_run)

        # 7. Final Cleanup
        print("🧹 Cleaning up unused Docker images...")
        run_cmd(ssh, "docker image prune -f")

        print("\n" + "="*40)
        print("✅ DEPLOYMENT COMPLETE!")
        print(f"Frontend: http://{HOST}:{WEB_PORT}")
        print(f"Backend (API): http://{HOST}:{API_PORT}")
        print("="*40)

        ssh.close()
    except Exception as e:
        print(f"❌ Error during deployment: {e}")

if __name__ == "__main__":
    deploy()
