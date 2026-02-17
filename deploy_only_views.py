import paramiko
import os
import base64
import logging
from dotenv import load_dotenv
import time

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')
REMOTE_BASE_PATH = '/volume1/docker/gundammap'

# 타임아웃 설정 (초)
SSH_TIMEOUT = 10
COMMAND_TIMEOUT = 30

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("Deploy")

def exec_command_with_timeout(client, command, timeout=COMMAND_TIMEOUT):
    """타임아웃이 있는 명령어 실행 (non-blocking 방식)"""
    try:
        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        channel = stdout.channel
        channel.settimeout(timeout)
        
        output = []
        error = []
        
        start_time = time.time()
        # 명령어 완료 대기 또는 타임아웃
        while not channel.exit_status_ready():
            if time.time() - start_time > timeout:
                logger.warning(f"Command timed out after {timeout}s: {command[:50]}...")
                break
            
            if channel.recv_ready():
                output.append(channel.recv(4096).decode('utf-8', errors='ignore'))
            if channel.recv_stderr_ready():
                error.append(channel.recv_stderr(4096).decode('utf-8', errors='ignore'))
            
            time.sleep(0.5)
            
        while channel.recv_ready():
            output.append(channel.recv(4096).decode('utf-8', errors='ignore'))
        while channel.recv_stderr_ready():
            error.append(channel.recv_stderr(4096).decode('utf-8', errors='ignore'))
            
        exit_status = channel.recv_exit_status() if channel.exit_status_ready() else -1
        full_output = "".join(output)
        full_error = "".join(error)
        
        return exit_status, full_output, full_error
    except Exception as e:
        logger.warning(f"SSH Command error: {e}")
        return -1, "", str(e)

def upload_file_chunked(client, local_path, remote_path):
    """파일을 청크 단위로 업로드"""
    if not os.path.exists(local_path):
        logger.warning(f"File not found: {local_path}")
        return False
    
    try:
        with open(local_path, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Step 1: 원격 파일 생성/초기화
        clear_cmd = f"echo {PASS} | sudo -S bash -c \"mkdir -p '{os.path.dirname(remote_path)}' && echo -n '' > '{remote_path}.tmp'\""
        exit_status, _, _ = exec_command_with_timeout(client, clear_cmd, timeout=10)
        if exit_status != 0:
            logger.error(f"Failed to create temp file for {remote_path}")
            return False
        
        # Step 2: base64 청크로 추가
        chunk_size = 4000
        total_chunks = (len(content_b64) + chunk_size - 1) // chunk_size
        for i in range(0, len(content_b64), chunk_size):
            chunk = content_b64[i:i+chunk_size]
            chunk_num = i // chunk_size + 1
            # logger.info(f"  Uploading chunk {chunk_num}/{total_chunks}...")
            
            sudo_append = f"echo {PASS} | sudo -S bash -c \"echo -n '{chunk}' >> '{remote_path}.tmp'\""
            exit_status, _, _ = exec_command_with_timeout(client, sudo_append, timeout=10)
            if exit_status != 0:
                logger.error(f"Failed to upload chunk {chunk_num}")
                return False
        
        # Step 3: 디코드 및 이동
        final_cmd = f"echo {PASS} | sudo -S bash -c \"base64 -d '{remote_path}.tmp' > '{remote_path}' && rm '{remote_path}.tmp'\""
        exit_status, _, error = exec_command_with_timeout(client, final_cmd, timeout=10)
        
        if exit_status == 0:
            logger.info(f"Successfully uploaded {remote_path}")
            return True
        else:
            logger.error(f"Failed to finalize {remote_path}: {error}")
            return False
    except Exception as e:
        logger.error(f"Error uploading {local_path}: {e}")
        return False

def deploy():
    """views.py만 배포"""
    files_to_deploy = [
        ('maps/views.py', 'maps/views.py'),
    ]
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.info(f"Connecting to {HOST}...")
        client.connect(HOST, username=USER, password=PASS, timeout=SSH_TIMEOUT)
        logger.info("Connected successfully\n")
        
        success_count = 0
        for rel_local, rel_remote in files_to_deploy:
            local_path = os.path.join(LOCAL_BASE_PATH, rel_local)
            remote_path = os.path.join(REMOTE_BASE_PATH, rel_remote).replace('\\', '/')
            
            if not os.path.exists(local_path):
                logger.warning(f"Skipping {rel_local} (not found locally)")
                continue
            
            logger.info(f"Deploying {rel_local}...")
            if upload_file_chunked(client, local_path, remote_path):
                success_count += 1
            else:
                logger.error(f"Failed to deploy {rel_local}")
        
        if success_count > 0:
            logger.info(f"\n{success_count}/{len(files_to_deploy)} files deployed successfully")
            
            # 컨테이너 재시작 (타임아웃 적용)
            logger.info("\nRestarting web container...")
            restart_cmd = f"echo {PASS} | sudo -S docker restart gundammap_web_1"
            exit_status, output, error = exec_command_with_timeout(client, restart_cmd, timeout=30)
            
            if exit_status == 0:
                logger.info("Container restarted successfully")
                logger.info("\n[OK] Deployment completed! Wait 5-10 seconds before accessing the site.")
            else:
                logger.warning(f"Restart may have issues: {error}")
        else:
            logger.error("No files were deployed successfully")
        
        client.close()
        
    except paramiko.SSHException as e:
        logger.error(f"SSH connection failed: {e}")
    except Exception as e:
        logger.error(f"Deployment failed: {e}")

if __name__ == "__main__":
    deploy()
