import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_bs4():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        print("Checking if beautifulsoup4 is installed...")
        
        # Check installed packages
        cmd = f'echo {PASS} | sudo -S /usr/local/bin/docker exec gundammap-web pip list | grep beautifulsoup'
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("Installed packages:")
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print("STDERR:", err)
        
        # Try to import in Python
        print("\nTrying to import bs4 in container...")
        cmd = f'echo {PASS} | sudo -S /usr/local/bin/docker exec gundammap-web python -c "from bs4 import BeautifulSoup; print(\'BS4 imported successfully\')"'
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print("STDERR:", err)
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_bs4()
