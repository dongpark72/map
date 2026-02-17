@echo off
chcp 65001 >nul
rem ========================================================
rem [v3.0 Deployment Script for GundamMap - Debian Server]
rem Server: 100.118.226.70
rem Frontend: 9002
rem Backend: 9092
rem DB: 9746
rem ========================================================

set REMOTE_HOST=175.126.187.60
set REMOTE_USER=pdi1972
set REMOTE_PASS=timess9746
set REMOTE_DIR=/srv/dev-disk-by-uuid-4b8dbcea-7516-4842-89b9-14865912be78/docker/gundammap
set PASSWORD=%REMOTE_PASS%

echo ==========================================
echo Starting Deployment to %REMOTE_HOST%...
echo ==========================================

cd /d e:\Antigravity\Gundammap

echo [1/6] Cleaning local temporary files...
del *.tmp 2>nul
del *.bak 2>nul

echo [2/6] Creating remote directory...
echo Connecting to %REMOTE_HOST% as %REMOTE_USER%...
plink -batch -ssh -pw %PASSWORD% %REMOTE_USER%@%REMOTE_HOST% "echo %PASSWORD% | sudo -S mkdir -p %REMOTE_DIR% && echo %PASSWORD% | sudo -S chown %REMOTE_USER%:%REMOTE_USER% %REMOTE_DIR%"
if errorlevel 1 (
    echo [ERROR] Connection failed. Please check your password or network connection.
    pause
    exit /b 1
)

echo [3/6] Uploading files...
rem Configuration Files
pscp -batch -scp -pw %PASSWORD% docker-compose-v3.yml %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/docker-compose.yml
pscp -batch -scp -pw %PASSWORD% backend.Dockerfile %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/backend.Dockerfile
pscp -batch -scp -pw %PASSWORD% frontend.Dockerfile %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/frontend.Dockerfile
pscp -batch -scp -pw %PASSWORD% Dockerfile_db_32bit %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/Dockerfile_db_32bit
pscp -batch -scp -pw %PASSWORD% nginx_custom.conf %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/nginx_custom.conf
pscp -batch -scp -pw %PASSWORD% requirements.txt %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/requirements.txt
pscp -batch -scp -pw %PASSWORD% .env %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/.env
pscp -batch -scp -pw %PASSWORD% manage.py %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/manage.py

rem Directories
echo Uploading Source Directories (This may take some time)...
pscp -batch -r -scp -pw %PASSWORD% gundammap %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/gundammap
pscp -batch -r -scp -pw %PASSWORD% maps %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/maps
pscp -batch -r -scp -pw %PASSWORD% templates %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%/templates

echo [4/6] Running Docker Compose on Remote...
rem Note: Using 'docker compose' (v2) or 'docker-compose' (v1) depending on availability
plink -batch -ssh -pw %PASSWORD% %REMOTE_USER%@%REMOTE_HOST% "cd %REMOTE_DIR% && echo %PASSWORD% | sudo -S docker compose down || docker-compose down || true"
plink -batch -ssh -pw %PASSWORD% %REMOTE_USER%@%REMOTE_HOST% "cd %REMOTE_DIR% && echo %PASSWORD% | sudo -S docker compose up -d --build || sudo -S docker-compose up -d --build"

echo [5/6] Cleaning up unused images/containers...
plink -batch -ssh -pw %PASSWORD% %REMOTE_USER%@%REMOTE_HOST% "echo %PASSWORD% | sudo -S docker image prune -f"
plink -batch -ssh -pw %PASSWORD% %REMOTE_USER%@%REMOTE_HOST% "echo %PASSWORD% | sudo -S docker container prune -f"

echo ==========================================
echo Deployment to Server Complete!
echo ==========================================
echo 🚀 Starting R2 Cloud Storage Sync...
python r2_sync_tool.py
pause
