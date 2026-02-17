import sys
import time
import os
import paramiko
import base64
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_BASE_PATH = '/volume1/docker/gundammap'
LOCAL_BASE_PATH = os.getcwd()

class RobustSyncHandler(FileSystemEventHandler):
    def __init__(self):
        self.client = None
        self.connect()

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(HOST, username=USER, password=PASS)
            print("Connected to NAS with SSH for robust syncing.")
        except Exception as e:
            print(f"Connection failed: {e}")

    def upload_via_ssh(self, local_path):
        rel_path = os.path.relpath(local_path, LOCAL_BASE_PATH)
        if rel_path.startswith('.') or 'venv' in rel_path or '__pycache__' in rel_path:
            return
            
        remote_path = os.path.join(REMOTE_BASE_PATH, rel_path).replace('\\', '/')
        
        try:
            with open(local_path, "rb") as f:
                content_b64 = base64.b64encode(f.read()).decode('utf-8')
            
            # Use base64 + sudo tee to bypass permission issues
            cmd = f"echo '{content_b64}' | base64 -d | sudo tee '{remote_path}' > /dev/null"
            
            print(f"Syncing: {rel_path}...")
            # We need to send password to sudo
            full_cmd = f"echo {PASS} | sudo -S bash -c \"mkdir -p '{os.path.dirname(remote_path)}' && echo '{content_b64}' | base64 -d > '{remote_path}'\""
            
            stdin, stdout, stderr = self.client.exec_command(full_cmd)
            exit_status = stdout.channel.recv_exit_status()
            
            if exit_status == 0:
                print(f" -> Success: {rel_path}")
            else:
                print(f" -> Failed: {stderr.read().decode()}")
                self.connect() # Try reconnecting
        except Exception as e:
            print(f"Error during sync: {e}")

    def on_modified(self, event):
        if not event.is_directory:
            self.upload_via_ssh(event.src_path)
            if event.src_path.endswith('.py'):
                print("Python file modified. Restarting container...")
                self.restart_container()

    def on_created(self, event):
        if not event.is_directory:
            self.upload_via_ssh(event.src_path)
            if event.src_path.endswith('.py'):
                print("Python file created. Restarting container...")
                self.restart_container()

    def restart_container(self):
        try:
            # Detect container name dynamically or use standard one
            restart_cmd = f"echo {PASS} | sudo -S docker restart gundammap-web-1 || echo {PASS} | sudo -S docker restart gundammap_web_1"
            stdin, stdout, stderr = self.client.exec_command(restart_cmd)
            stdout.read() # wait
            print("Web container restarted.")
        except Exception as e:
            print(f"Error restarting container: {e}")

if __name__ == "__main__":
    path = LOCAL_BASE_PATH
    event_handler = RobustSyncHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    print(f"Monitoring {path} for changes (Robust Mode)...")
    
    # Initial Force Sync for index.html
    index_path = os.path.join(LOCAL_BASE_PATH, 'templates', 'maps', 'index.html')
    if os.path.exists(index_path):
        event_handler.upload_via_ssh(index_path)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
