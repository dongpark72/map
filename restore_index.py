import paramiko

HOST = '175.126.187.59'
PORT = 22
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap/templates/maps/index.html'
LOCAL_PATH = 'e:/Antigravity/Gundammap/templates/maps/index.html'

def restore_from_server_cat():
    print("=" * 60)
    print("🚑 Restoring index.html from Server (via cat)")
    print("=" * 60)
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, PORT, USER, PASS, timeout=10)
        
        # Check if file exists
        stdin, stdout, stderr = client.exec_command(f'ls -l {REMOTE_PATH}')
        ls_out = stdout.read().decode()
        print(f"ls output: {ls_out}")
        
        if "No such file" in ls_out or not ls_out.strip():
             print("File not found on server!")
             return

        # cat content
        stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_PATH}')
        content = stdout.read().decode() # Adjust encoding if needed, usually utf-8
        
        if content:
            with open(LOCAL_PATH, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Restored {len(content)} bytes to {LOCAL_PATH}")
        else:
            print("❌ Empty content retrieved!")
            
        client.close()
        
    except Exception as e:
        print(f"❌ Restore Failed: {e}")

if __name__ == "__main__":
    restore_from_server_cat()
