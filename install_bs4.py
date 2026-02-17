import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def install_bs4():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        print("Installing beautifulsoup4 in Docker container...")
        
        # Install beautifulsoup4 in the web container
        cmd = f'echo {PASS} | sudo -S /usr/local/bin/docker exec gundammap-web pip install beautifulsoup4>=4.12'
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("STDOUT:")
        print(stdout.read().decode())
        print("\nSTDERR:")
        print(stderr.read().decode())
        
        # Restart the web container
        print("\nRestarting web container...")
        cmd = f'cd /volume1/docker/gundammap && echo {PASS} | sudo -S /usr/local/bin/docker-compose restart web'
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("\nDone! BeautifulSoup4 should now be installed.")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    install_bs4()
