import paramiko

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def run_migration():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        # 마이그레이션 파일 업로드
        sftp = client.open_sftp()
        sftp.chdir('/volume1/docker/gundammap/maps/migrations')
        local_migration = r'E:\Antigravity\Gundammap\maps\migrations\0004_landinfocache_alter_parcelcache_options_and_more.py'
        sftp.put(local_migration, '0004_landinfocache_alter_parcelcache_options_and_more.py')
        print("Migration file uploaded")
        sftp.close()
        
        # utils.py 업로드
        sftp = client.open_sftp()
        sftp.chdir('/volume1/docker/gundammap/maps')
        local_utils = r'E:\Antigravity\Gundammap\maps\utils.py'
        sftp.put(local_utils, 'utils.py')
        print("utils.py uploaded")
        sftp.close()
        
        # models.py 업로드
        sftp = client.open_sftp()
        sftp.chdir('/volume1/docker/gundammap/maps')
        local_models = r'E:\Antigravity\Gundammap\maps\models.py'
        sftp.put(local_models, 'models.py')
        print("models.py uploaded")
        sftp.close()
        
        # 마이그레이션 실행
        cmd = f"echo {PASS} | sudo -S docker exec gundammap_web_1 python manage.py migrate"
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        print("Migration output:")
        print(output)
        if error:
            print("Migration errors:")
            print(error)
        
        # 컨테이너 재시작
        cmd = f"echo {PASS} | sudo -S docker restart gundammap_web_1"
        client.exec_command(cmd)
        print("Container restarted")
        
        client.close()
        print("\n✅ All done!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_migration()
