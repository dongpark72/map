@echo off
rem ========================================================
rem [Configuration]
rem ========================================================
set PROJECT_NAME=gundammap
set WEB_PORT=8004
set API_PORT=8084
set WEB_CONTAINER=gundammap-front
set API_CONTAINER=gundammap-backend
set NETWORK_NAME=gundammap-net
rem ========================================================

set SERVER_IP=175.126.187.59
set PASSWORD=timess9746
set USER=dongpark72
set REMOTE_PATH=/volume1/docker/%PROJECT_NAME%

echo ==========================================
echo %PROJECT_NAME% Deployment
echo Network: %NETWORK_NAME%
echo Web: %WEB_PORT% / API: %API_PORT%
echo ==========================================

echo [1/5] Uploading Configs & Scripts...
pscp -batch -scp -pw %PASSWORD% nginx_custom.conf %USER%@%SERVER_IP%:%REMOTE_PATH%/nginx_custom.conf
pscp -batch -scp -pw %PASSWORD% Dockerfile %USER%@%SERVER_IP%:%REMOTE_PATH%/Dockerfile
pscp -batch -scp -pw %PASSWORD% backend.Dockerfile %USER%@%SERVER_IP%:%REMOTE_PATH%/Dockerfile.backend
pscp -batch -scp -pw %PASSWORD% requirements.txt %USER%@%SERVER_IP%:%REMOTE_PATH%/requirements.txt
pscp -batch -scp -pw %PASSWORD% .env %USER%@%SERVER_IP%:%REMOTE_PATH%/.env
pscp -batch -scp -r -pw %PASSWORD% . %USER%@%SERVER_IP%:%REMOTE_PATH%

echo [2/5] Creating Docker Network...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker network create %NETWORK_NAME% || true"

echo [3/5] Cleaning Old Containers...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker rm -f %WEB_CONTAINER% %API_CONTAINER% || true"

echo [4/5] Starting Backend (%API_CONTAINER%)...
rem Note: Mapping API_PORT to 8000 because Django runserver listens on 8000
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker build -f Dockerfile.backend -t %API_CONTAINER% . && echo %PASSWORD% | sudo -S docker run -d -p %API_PORT%:8000 --name %API_CONTAINER% --network %NETWORK_NAME% --restart unless-stopped %API_CONTAINER%"

echo [5/5] Starting Frontend (%WEB_CONTAINER%)...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker build -t %WEB_CONTAINER% . && echo %PASSWORD% | sudo -S docker run -d -p %WEB_PORT%:80 --name %WEB_CONTAINER% --network %NETWORK_NAME% --restart unless-stopped %WEB_CONTAINER%"

echo Done!
echo 🚀 Starting R2 Cloud Storage Sync...
python r2_sync_tool.py
pause
