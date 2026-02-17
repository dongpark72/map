import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def test_local_url():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    
    # Try fetching the URL from inside the web container
    cmd = f"echo {PASS} | sudo -S /usr/local/bin/docker exec gundammap_web_1 curl -s http://localhost:8000/proxy/landinfo/?pnu=2671034027100080001"
    stdin, stdout, stderr = client.exec_command(cmd)
    
    print("--- Output ---")
    print(stdout.read().decode())
    print("--- Error ---")
    print(stderr.read().decode())
    
    client.close()

if __name__ == "__main__":
    test_local_url()
