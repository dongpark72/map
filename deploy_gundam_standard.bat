@echo off
rem ========================================================
rem [Standard Deployment Script for GundamMap]
rem Based on .agent-deploy-guide.md
rem ========================================================
set PROJECT_NAME=gundammap
set WEB_PORT=8000
set WEB_CONTAINER=gundam-web
set DB_CONTAINER=gundam-db
set NETWORK_NAME=gundam-net
rem ========================================================

set SERVER_IP=175.126.187.59
set PASSWORD=timess9746
set USER=dongpark72
set REMOTE_PATH=/volume1/docker/%PROJECT_NAME%

echo ==========================================
echo %PROJECT_NAME% Standard Deployment
echo Network: %NETWORK_NAME%
echo Web: %WEB_PORT%
echo ==========================================

echo [1/7] Cleaning up old temporary files...
del *.tmp 2>nul

echo [1.5/7] Creating remote directory...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "mkdir -p %REMOTE_PATH%"

echo [2/7] Uploading source code...
pscp -batch -scp -pw %PASSWORD% Dockerfile %USER%@%SERVER_IP%:%REMOTE_PATH%/Dockerfile
pscp -batch -scp -pw %PASSWORD% Dockerfile.db %USER%@%SERVER_IP%:%REMOTE_PATH%/Dockerfile.db
pscp -batch -scp -pw %PASSWORD% requirements.txt %USER%@%SERVER_IP%:%REMOTE_PATH%/requirements.txt
pscp -batch -scp -pw %PASSWORD% .env %USER%@%SERVER_IP%:%REMOTE_PATH%/.env
pscp -batch -scp -pw %PASSWORD% manage.py %USER%@%SERVER_IP%:%REMOTE_PATH%/manage.py

echo Uploading folders (this may take a moment)...
pscp -batch -r -scp -pw %PASSWORD% gundammap %USER%@%SERVER_IP%:%REMOTE_PATH%/gundammap
pscp -batch -r -scp -pw %PASSWORD% maps %USER%@%SERVER_IP%:%REMOTE_PATH%/maps
pscp -batch -r -scp -pw %PASSWORD% templates %USER%@%SERVER_IP%:%REMOTE_PATH%/templates

echo [3/7] Creating Docker Network...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker network create %NETWORK_NAME% || true"

echo [4/7] Stopping Old Containers...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker rm -f %WEB_CONTAINER% %DB_CONTAINER% gundammap_web_1 gundammap_db_1 || true"

echo [5/7] Building & Starting Database...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker build -f Dockerfile.db -t %DB_CONTAINER% ."
rem Pass mapped env vars manually for Postgres
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker run -d --name %DB_CONTAINER% --network %NETWORK_NAME% --restart always --env-file .env -e POSTGRES_DB=gundammap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=timess9746 -v gundammap_postgres_data:/var/lib/postgresql/data %DB_CONTAINER%"

echo [6/7] Building & Starting Web (Django)...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker build -t %WEB_CONTAINER% ."
rem Override DB_HOST to point to new container name
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker run -d -p %WEB_PORT%:8000 --name %WEB_CONTAINER% --network %NETWORK_NAME% --restart always --env-file .env -e DB_HOST=%DB_CONTAINER% -v %REMOTE_PATH%:/app %WEB_CONTAINER% python manage.py runserver 0.0.0.0:8000"

echo [7/7] Verifying...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker ps --filter name=%PROJECT_NAME% --filter name=%WEB_CONTAINER% --filter name=%DB_CONTAINER%"

echo Done!
echo 🚀 Starting R2 Cloud Storage Sync...
python r2_sync_tool.py
pause
