@echo off
rem ========================================================
rem [Split Deployment Script for GundamMap]
rem Frontend: 8004 (Nginx)
rem Backend: 8084 (Django)
rem Database: Internal
rem ========================================================
set PROJECT_NAME=gundammap
set FRONT_PORT=8004
set BACK_PORT=8084
set FRONT_CONTAINER=gundammap-frontend
set BACK_CONTAINER=gundammap-backend
set DB_CONTAINER=gundam-db
set NETWORK_NAME=gundam-net
rem ========================================================

set SERVER_IP=175.126.187.59
set PASSWORD=timess9746
set USER=dongpark72
set REMOTE_PATH=/volume1/docker/%PROJECT_NAME%

echo ==========================================
echo %PROJECT_NAME% Split Deployment
echo Network: %NETWORK_NAME%
echo Frontend: %FRONT_PORT%
echo Backend: %BACK_PORT%
echo ==========================================

echo [1/8] Cleaning up old temporary files...
del *.tmp 2>nul

echo [1.5/8] Creating remote directory...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "mkdir -p %REMOTE_PATH%"

echo [2/8] Uploading source code...
pscp -batch -scp -pw %PASSWORD% backend.Dockerfile %USER%@%SERVER_IP%:%REMOTE_PATH%/backend.Dockerfile
pscp -batch -scp -pw %PASSWORD% frontend.Dockerfile %USER%@%SERVER_IP%:%REMOTE_PATH%/frontend.Dockerfile
pscp -batch -scp -pw %PASSWORD% Dockerfile.db %USER%@%SERVER_IP%:%REMOTE_PATH%/Dockerfile.db
pscp -batch -scp -pw %PASSWORD% nginx_custom.conf %USER%@%SERVER_IP%:%REMOTE_PATH%/nginx_custom.conf
pscp -batch -scp -pw %PASSWORD% requirements.txt %USER%@%SERVER_IP%:%REMOTE_PATH%/requirements.txt
pscp -batch -scp -pw %PASSWORD% .env %USER%@%SERVER_IP%:%REMOTE_PATH%/.env
pscp -batch -scp -pw %PASSWORD% manage.py %USER%@%SERVER_IP%:%REMOTE_PATH%/manage.py

echo Uploading folders (this may take a moment)...
pscp -batch -r -scp -pw %PASSWORD% gundammap %USER%@%SERVER_IP%:%REMOTE_PATH%/gundammap
pscp -batch -r -scp -pw %PASSWORD% maps %USER%@%SERVER_IP%:%REMOTE_PATH%/maps
pscp -batch -r -scp -pw %PASSWORD% templates %USER%@%SERVER_IP%:%REMOTE_PATH%/templates

echo [3/8] Creating Docker Network...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker network create %NETWORK_NAME% || true"

echo [4/8] Stopping Old Containers...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker rm -f %FRONT_CONTAINER% %BACK_CONTAINER% %DB_CONTAINER% gundam-web || true"

echo [5/8] Building & Starting Database...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker build -f Dockerfile.db -t %DB_CONTAINER% ."
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker run -d --name %DB_CONTAINER% --network %NETWORK_NAME% --restart always --env-file .env -e POSTGRES_DB=gundammap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=timess9746 -v gundammap_postgres_data:/var/lib/postgresql/data %DB_CONTAINER%"

echo [6/8] Building & Starting Backend (Django)...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker build -f backend.Dockerfile -t %BACK_CONTAINER% ."
rem Running Backend on 8084
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker run -d -p %BACK_PORT%:8000 --name %BACK_CONTAINER% --network %NETWORK_NAME% --restart always --env-file .env -e DB_HOST=%DB_CONTAINER% -v %REMOTE_PATH%:/app %BACK_CONTAINER% python manage.py runserver 0.0.0.0:8000"

echo [7/8] Building & Starting Frontend (Nginx)...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker build -f frontend.Dockerfile -t %FRONT_CONTAINER% ."
rem Running Frontend on 8004
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker run -d -p %FRONT_PORT%:80 --name %FRONT_CONTAINER% --network %NETWORK_NAME% --restart always %FRONT_CONTAINER%"

echo [8/8] Verifying...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker ps --filter name=%FRONT_CONTAINER% --filter name=%BACK_CONTAINER%"

echo Done! Deployment Complete on 8004 (Front) and 8084 (Back).
echo 🚀 Starting R2 Cloud Storage Sync...
python r2_sync_tool.py
pause
