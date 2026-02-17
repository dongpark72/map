import paramiko
HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
print(f"Connecting to {HOST}...")
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS, timeout=10)
    print("Connected successfully!")
    stdin, stdout, stderr = client.exec_command('ls -la /volume1/docker/gundammap')
    print(stdout.read().decode())
    client.close()
except Exception as e:
    print(f"Failed: {e}")
