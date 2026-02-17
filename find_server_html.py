import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def find_html_file():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    # Find the index.html file
    cmd = "find /volume1/docker/gundammap -name 'index.html' -type f 2>/dev/null"
    stdin, stdout, stderr = client.exec_command(cmd)
    files = stdout.read().decode().strip().split('\n')
    
    print("Found index.html files:")
    for f in files:
        if f:
            print(f"  {f}")
    
    # Check docker container structure
    cmd = "ls -la /volume1/docker/gundammap/"
    stdin, stdout, stderr = client.exec_command(cmd)
    print("\n/volume1/docker/gundammap/ contents:")
    print(stdout.read().decode())
    
    client.close()

if __name__ == "__main__":
    find_html_file()
