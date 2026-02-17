import datetime
from r2_sync_tool import R2Uploader

# Configuration
BACKUP_DIR = os.path.join("backups", "v3.1")
os.makedirs(BACKUP_DIR, exist_ok=True)

FILES_TO_BACKUP = [
    "maps/models.py",
    "maps/views.py",
    "maps/urls.py",
    "templates/maps/map_app.html",
    "templates/maps/index.html",
    "gundammap/settings.py",
    ".env",
    "nginx_custom.conf",
    "frontend.Dockerfile",
    "backend.Dockerfile"
]

# Generate Docker Compose for v3.1 standard
DOCKER_COMPOSE_CONTENT = """version: '3.8'

services:
  # Frontend (Nginx) - Port 8004
  frontend:
    build:
      context: .
      dockerfile: frontend.Dockerfile
    container_name: gundammap-front
    ports:
      - "8004:80"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - gundammap-net

  # Backend (Django) - Port 8084
  backend:
    build:
      context: .
      dockerfile: backend.Dockerfile
    container_name: gundammap-backend
    ports:
      - "8084:8000"
    volumes:
      - .:/app
    env_file:
      - .env
    environment:
      - DB_HOST=gundammap-db
      - USE_POSTGRES=True
    depends_on:
      - db
    restart: unless-stopped
    networks:
      - gundammap-net

  # Database (PostgreSQL) - Port 5432 (Internal)
  db:
    image: postgis/postgis:15-3.3
    container_name: gundammap-db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env
    restart: unless-stopped
    networks:
      - gundammap-net

volumes:
  postgres_data:

networks:
  gundammap-net:
    driver: bridge
"""

def perform_backup():
    print(f"📂 Starting Backup to {BACKUP_DIR}...")
    
    # 1. Copy Files
    for file_path in FILES_TO_BACKUP:
        if os.path.exists(file_path):
            target_path = os.path.join(BACKUP_DIR, file_path.replace("/", "_").replace("\\", "_"))
            # Preserve original folder structure if preferred, but usually flat or minimal is ok.
            # Let's simple copy to root of backup dir for easy access, or keep structure?
            # Previous backups (v2.5) seem to have flattened names like templates_maps_map_app.html
            
            shutil.copy2(file_path, target_path)
            print(f"  ✅ Copied: {file_path}")
        else:
            print(f"  ⚠️ File not found: {file_path}")

    # 2. Save Docker Compose v3.1
    compose_path = os.path.join(BACKUP_DIR, "docker-compose.yml")
    with open(compose_path, "w", encoding="utf-8") as f:
        f.write(DOCKER_COMPOSE_CONTENT)
    print(f"  ✅ Generated: docker-compose.yml (v3.1 Standard)")

    # 3. Create Info File
    info_path = os.path.join(BACKUP_DIR, "backup_info.txt")
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(f"""Backup Version: v3.1
Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== Changes in v3.1 ===
1. Architecture Change:
   - Split into Frontend (Nginx) and Backend (Django) containers.
   - Frontend Port: 8004
   - Backend Port: 8084
   - DB Port: 5432 (Internal)

2. Deployment:
   - Applied standard deployment guide conventions.
   - Cleaned up old containers (gundammap_web_1, etc).

3. Files:
   - Added nginx_custom.conf
   - Added frontend.Dockerfile
   - Updated docker-compose.yml to reflect split architecture.
""")
    print(f"  ✅ Created: backup_info.txt")
    # 4. Sync to Cloudflare R2 (Optional/Auto)
    print("\n☁️ Syncing to Cloudflare R2...")
    uploader = R2Uploader()
    if uploader.enabled:
        # 백업 폴더 내의 모든 파일을 R2로 전송
        for root, dirs, files in os.walk(BACKUP_DIR):
            for file in files:
                local_full_path = os.path.join(root, file)
                # backups/v3.1/filename -> r2_backups/v3.1/filename
                remote_path = local_full_path.replace("\\", "/")
                uploader.upload_file(local_full_path, remote_path)
        print("✅ Cloud Backup Complete!")
    else:
        print("ℹ️ R2 upload skipped (Settings missing in .env)")

    print(f"\n🎉 Backup Complete!")

if __name__ == "__main__":
    perform_backup()
