@echo off
rem ========================================================
rem [Full Rebuild and Deploy for CDN]
rem ========================================================
set PROJECT_NAME=gundammap
set SERVER_IP=175.126.187.59
set PASSWORD=timess9746
set USER=dongpark72
set REMOTE_PATH=/volume1/docker/%PROJECT_NAME%

echo ==========================================
echo Full Rebuild and Deploy for CDN
echo Target: %SERVER_IP%
echo ==========================================

echo [1/6] Uploading all project files...
pscp -batch -scp -r -pw %PASSWORD% . %USER%@%SERVER_IP%:%REMOTE_PATH%

echo [2/6] Stopping containers...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker stop gundammap-backend gundammap-frontend || true"

echo [3/6] Removing old containers...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker rm gundammap-backend gundammap-frontend || true"

echo [4/6] Rebuilding backend...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker build -f backend.Dockerfile -t gundammap-backend ."

echo [5/6] Rebuilding frontend...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "cd %REMOTE_PATH% && echo %PASSWORD% | sudo -S docker build -f Dockerfile -t gundammap-frontend ."

echo [6/6] Starting containers...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker run -d -p 8084:8000 --name gundammap-backend --network gundammap-net --restart unless-stopped gundammap-backend"
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker run -d -p 8004:80 --name gundammap-frontend --network gundammap-net --restart unless-stopped gundammap-frontend"

echo.
echo ==========================================
echo Deployment Complete!
echo ==========================================
echo.
echo Please wait 30 seconds for containers to start.
echo Then check: https://map.goal-runner.com/portal/
echo.
pause
