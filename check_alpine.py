import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_alpine():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    docker_bin = "/usr/local/bin/docker"
    
    tags = [
        "python:3.11-alpine",
        "postgis/postgis:15-3.3-alpine"
    ]
    
    for tag in tags:
        print(f"Testing {tag}...")
        stdin, stdout, stderr = client.exec_command(f'echo {PASS} | sudo -S {docker_bin} pull {tag}')
        if stdout.channel.recv_exit_status() == 0:
            print("SUCCESS")
        else:
            print("FAIL")
            print(stderr.read().decode())
            
    client.close()

if __name__ == "__main__":
    check_alpine()
