import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def test_python_pull():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    docker_bin = "/usr/local/bin/docker"
    
    tags = ["python:3.11-slim-bookworm", "python:3.11-alpine", "python:3.11"]
    
    for tag in tags:
        print(f"Testing pull {tag}...")
        cmd = f'echo {PASS} | sudo -S {docker_bin} pull {tag}'
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Read exit status
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print(f"SUCCESS: {tag}")
        else:
            print(f"FAIL: {tag}")
            print(stderr.read().decode())
            
    client.close()

if __name__ == "__main__":
    test_python_pull()
