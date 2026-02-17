import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def checks():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    docker_bin = "/usr/local/bin/docker"
    
    tags = [
        "python:3.10-slim-buster",
        "postgis/postgis:15-3.3-alpine"
    ]
    
    for tag in tags:
        print(f"Testing {tag}...")
        cmd = f'echo {PASS} | sudo -S {docker_bin} pull {tag}'
        stdin, stdout, stderr = client.exec_command(cmd)
        if stdout.channel.recv_exit_status() == 0:
            print("SUCCESS")
        else:
            print("FAIL")
            print(stderr.read().decode())
            
    client.close()

if __name__ == "__main__":
    checks()
