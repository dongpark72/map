@echo off
rem ========================================================
rem [CDN Update Deployment - Quick Deploy]
rem ========================================================
set PROJECT_NAME=gundammap
set SERVER_IP=175.126.187.59
set PASSWORD=timess9746
set USER=dongpark72
set REMOTE_PATH=/volume1/docker/%PROJECT_NAME%

echo ==========================================
echo CDN Configuration Update Deployment
echo Target: %SERVER_IP%
echo ==========================================

echo [1/3] Uploading updated settings.py...
pscp -batch -scp -pw %PASSWORD% gundammap\settings.py %USER%@%SERVER_IP%:%REMOTE_PATH%/gundammap/settings.py

echo [2/3] Uploading .env file...
pscp -batch -scp -pw %PASSWORD% .env %USER%@%SERVER_IP%:%REMOTE_PATH%/.env

echo [3/3] Restarting containers...
plink -batch -ssh -pw %PASSWORD% %USER%@%SERVER_IP% "echo %PASSWORD% | sudo -S docker restart gundammap-backend gundammap-front || true"

echo.
echo ==========================================
echo Deployment Complete!
echo ==========================================
echo.
echo Please wait 10-20 seconds for containers to restart.
echo Then check: https://map.goal-runner.com/portal/
echo.
pause
