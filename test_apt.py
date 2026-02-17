import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def test_network_inside():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        docker_bin = "/usr/local/bin/docker"

        # Run a temporary container to test apt
        # python:3.11-slim-bookworm is Debian 12
        print("Testing apt-get inside container...")
        img = "public.ecr.aws/docker/library/python:3.11-slim-bookworm"
        cmd = f"echo {PASS} | sudo -S {docker_bin} run --rm {img} apt-get update"
        
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode()
        err = stderr.read().decode()
        print("STDOUT:", out)
        print("STDERR:", err)
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_network_inside()
