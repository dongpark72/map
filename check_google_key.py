import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_google_key():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        # More robust way to check settings
        cmd = f"echo {PASS} | sudo -S docker exec gundammap_web_1 python -c \"import os; from django.conf import settings; import django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gundammap.settings'); django.setup(); print('KEY_VAL:', settings.GOOGLE_MAPS_API_KEY[:10] if settings.GOOGLE_MAPS_API_KEY else 'NONE')\""
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_google_key()
