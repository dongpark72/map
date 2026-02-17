import paramiko
import os
import base64
import logging
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Configuration from Environment Variables
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))
HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')
REMOTE_BASE_PATH = '/volume1/docker/gundammap'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PortalFixDeploy")

def upload_file_chunked(client, local_path, remote_path):
    if not os.path.exists(local_path):
        logger.warning(f"File not found: {local_path}")
        return False
    
    try:
        with open(local_path, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Step 1: Create or clear the remote file
        clear_cmd = f"echo {PASS} | sudo -S bash -c \"mkdir -p '{os.path.dirname(remote_path)}' && echo -n '' > '{remote_path}.tmp'\""
        client.exec_command(clear_cmd)[1].channel.recv_exit_status()
        
        # Step 2: Append base64 in chunks
        chunk_size = 4000
        for i in range(0, len(content_b64), chunk_size):
            chunk = content_b64[i:i+chunk_size]
            sudo_append = f"echo {PASS} | sudo -S bash -c \"echo -n '{chunk}' >> '{remote_path}.tmp'\""
            client.exec_command(sudo_append)[1].channel.recv_exit_status()
        
        # Step 3: Decode and move
        final_cmd = f"echo {PASS} | sudo -S bash -c \"base64 -d '{remote_path}.tmp' > '{remote_path}' && rm '{remote_path}.tmp'\""
        stdin, stdout, stderr = client.exec_command(final_cmd)
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            logger.info(f"Successfully uploaded {remote_path}")
            return True
        else:
            logger.error(f"Failed to upload {remote_path}: {stderr.read().decode()}")
            return False
    except Exception as e:
        logger.error(f"Error uploading {local_path}: {e}")
        return False

def deploy_fix():
    # 현재 로컬 소스코드를 서버에 배포하여 /portal/ 경로 및 로그인 관련 설정 복구
    files_to_sync = [
        ('maps/urls.py', 'maps/urls.py'),
        ('maps/views.py', 'maps/views.py'),
        ('templates/maps/map_app.html', 'templates/maps/map_app.html'),
        ('templates/maps/index.html', 'templates/maps/index.html'),
    ]
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        logger.info("=== Starting Portal & Login Fix Deployment ===")
        
        success_count = 0
        for rel_local, rel_remote in files_to_sync:
            local = os.path.join(LOCAL_BASE_PATH, rel_local)
            remote = os.path.join(REMOTE_BASE_PATH, rel_remote).replace('\\', '/')
            if upload_file_chunked(client, local, remote):
                success_count += 1
        
        if success_count > 0:
            logger.info("Restarting web container...")
            # Try both possible container names
            restart_cmd = f"echo {PASS} | sudo -S docker restart gundammap-web-1 || echo {PASS} | sudo -S docker restart gundammap_web_1"
            client.exec_command(restart_cmd)[1].channel.recv_exit_status()
            logger.info("Web container restarted.")
            logger.info(f"=== Fix deployment completed: {success_count}/{len(files_to_sync)} files uploaded ===")
        else:
            logger.error("No files were uploaded successfully.")
        
        client.close()
        print("\n✅ /portal/ 및 /login/ 경로 복구 배포가 완료되었습니다!")
    except Exception as e:
        logger.error(f"Deployment failed: {e}")

if __name__ == "__main__":
    deploy_fix()
