import paramiko
HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
print(f"Connecting to {HOST}...")
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    stdin, stdout, stderr = client.exec_command('grep -C 5 "closePricePanel" /volume1/docker/gundammap/templates/maps/index.html')
    print("--- Server file content check ---")
    print(stdout.read().decode())
    client.close()
except Exception as e:
    print(f"Failed: {e}")
