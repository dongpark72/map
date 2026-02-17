import paramiko
HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS)
    stdin, stdout, stderr = client.exec_command('ls -R /volume1/docker/gundammap/templates')
    print(stdout.read().decode())
    client.close()
except Exception as e:
    print(e)
