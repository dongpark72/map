import paramiko
import os
import base64
import logging
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')
REMOTE_BASE_PATH = '/volume1/docker/gundammap'

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("FixModels")

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

def fix_models():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.info(f"Connecting to {HOST}...")
        client.connect(HOST, username=USER, password=PASS)
        logger.info("Connected successfully")
        
        # Upload models.py
        local_models = os.path.join(LOCAL_BASE_PATH, 'maps', 'models.py')
        remote_models = os.path.join(REMOTE_BASE_PATH, 'maps', 'models.py').replace('\\', '/')
        
        logger.info("Uploading models.py...")
        if upload_file_chunked(client, local_models, remote_models):
            logger.info("models.py uploaded successfully")
            
            # Run migrations
            logger.info("Running Django migrations...")
            migrate_cmd = f"echo {PASS} | sudo -S docker exec gundammap_web_1 python manage.py makemigrations"
            stdin, stdout, stderr = client.exec_command(migrate_cmd)
            stdout.channel.recv_exit_status()
            logger.info(stdout.read().decode('utf-8', errors='ignore'))
            
            migrate_cmd2 = f"echo {PASS} | sudo -S docker exec gundammap_web_1 python manage.py migrate"
            stdin, stdout, stderr = client.exec_command(migrate_cmd2)
            stdout.channel.recv_exit_status()
            logger.info(stdout.read().decode('utf-8', errors='ignore'))
            
            # Restart container
            logger.info("Restarting web container...")
            restart_cmd = f"echo {PASS} | sudo -S docker restart gundammap_web_1"
            client.exec_command(restart_cmd)[1].channel.recv_exit_status()
            logger.info("Container restarted")
            
            logger.info("Fix completed! Please wait 5-10 seconds and try accessing the site again.")
        else:
            logger.error("Failed to upload models.py")
        
        client.close()
        
    except Exception as e:
        logger.error(f"Fix failed: {e}")

if __name__ == "__main__":
    fix_models()
