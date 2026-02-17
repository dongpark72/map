import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def check_django_settings():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        # Simpler check
        cmd = f"echo {PASS} | sudo -S docker exec gundammap_web_1 python -c \"import os; from dotenv import load_dotenv; load_dotenv('.env'); print('VWORLD_IN_OS:', os.getenv('VWORLD_API_KEY')[:5] if os.getenv('VWORLD_API_KEY') else 'None')\""
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("--- OS ENV CHECK ---")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_django_settings()
