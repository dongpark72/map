import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def probe_docker():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        # Find docker
        # Try common paths
        paths = [
            "/usr/local/bin/docker",
            "/bin/docker",
            "/usr/bin/docker",
            "/var/packages/Docker/target/usr/bin/docker"
        ]
        
        docker_path = "docker" # default
        for p in paths:
             stdin, stdout, stderr = client.exec_command(f"ls {p}")
             if stdout.read().decode().strip() == p:
                 docker_path = p
                 break
        
        print(f"Docker found at: {docker_path}")
        
        # Test Pull
        print("Testing pull hello-world...")
        cmd = f'echo {PASS} | sudo -S {docker_path} pull hello-world'
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode()
        err = stderr.read().decode()
        print("STDOUT:", out)
        print("STDERR:", err)
        
        client.close()
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    probe_docker()
