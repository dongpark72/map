
import paramiko
import os
from dotenv import load_dotenv

LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(LOCAL_BASE_PATH, ".env"))

HOST = os.getenv('NAS_HOST', '175.126.187.59')
USER = os.getenv('NAS_USER', 'dongpark72')
PASS = os.getenv('NAS_PASS', 'timess9746')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, password=PASS)

cmd = f"cat /volume1/docker/gundammap/.env"
stdin, stdout, stderr = client.exec_command(cmd)
print("Remote .env content:")
print(stdout.read().decode())
client.close()
