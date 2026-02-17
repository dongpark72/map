import paramiko
import os
import base64

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_files():
    output = []
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        # Check .env on NAS
        cmd = "cat /volume1/docker/gundammap/.env"
        stdin, stdout, stderr = client.exec_command(cmd)
        output.append("--- NAS .env File ---")
        output.append(stdout.read().decode())
        
        # Check settings.py on NAS
        cmd = "cat /volume1/docker/gundammap/gundammap/settings.py"
        stdin, stdout, stderr = client.exec_command(cmd)
        output.append("--- NAS settings.py File ---")
        output.append(stdout.read().decode())
        
        # Check if environment variables are actually loaded in the container
        cmd = f"echo {PASS} | sudo -S docker exec gundammap_web_1 env | grep VWORLD"
        stdin, stdout, stderr = client.exec_command(cmd)
        output.append("--- Container Environment Variables ---")
        output.append(stdout.read().decode())
        
        client.close()
    except Exception as e:
        output.append(f"Error: {e}")
        
    with open('e:/Antigravity/Gundammap/nas_check_env.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

if __name__ == "__main__":
    check_files()
