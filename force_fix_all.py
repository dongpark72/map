import paramiko
import os
import base64

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def force_upload_all():
    files_to_upload = [
        ('e:/Antigravity/Gundammap/.env', '/volume1/docker/gundammap/.env'),
        ('e:/Antigravity/Gundammap/gundammap/settings.py', '/volume1/docker/gundammap/gundammap/settings.py'),
        ('e:/Antigravity/Gundammap/maps/views.py', '/volume1/docker/gundammap/maps/views.py'),
        ('e:/Antigravity/Gundammap/templates/maps/index.html', '/volume1/docker/gundammap/templates/maps/index.html')
    ]
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        for local, remote in files_to_upload:
            if not os.path.exists(local):
                print(f"File not found: {local}")
                continue
            with open(local, "rb") as f:
                content_b64 = base64.b64encode(f.read()).decode('utf-8')
            
            full_cmd = f"echo {PASS} | sudo -S bash -c \"mkdir -p '{os.path.dirname(remote)}' && echo '{content_b64}' | base64 -d > '{remote}'\""
            stdin, stdout, stderr = client.exec_command(full_cmd)
            stdout.read()
            print(f"Uploaded {os.path.basename(local)}")
            
        # Restart web container to make sure .env is picked up
        cmd = f"echo {PASS} | sudo -S docker restart gundammap_web_1"
        client.exec_command(cmd)
        print("Web container restarted.")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_upload_all()
