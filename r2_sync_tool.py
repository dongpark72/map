import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# ENV 로드
load_dotenv()

class R2Uploader:
    def __init__(self):
        self.access_key = os.getenv("R2_ACCESS_KEY_ID")
        self.secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("R2_BUCKET_NAME")
        self.endpoint_url = os.getenv("R2_ENDPOINT_URL")
        self.server_prefix = os.getenv("R2_SERVER_PREFIX", "unknown")
        
        if not all([self.access_key, self.secret_key, self.bucket_name, self.endpoint_url]):
            print(f"[WARNING] [{self.server_prefix}] R2 configuration missing in .env file.")
            self.enabled = False
        else:
            self.enabled = True
            self.s3_client = boto3.client(
                's3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name='auto'
            )

    def upload_file(self, local_file_path, remote_path=None):
        if not self.enabled:
            return False
            
        filename = os.path.basename(local_file_path)
        if filename == ".env":
            print(f"[SECURITY] Upload blocked: '{local_file_path}' (.env exclusion rule)")
            return False

        if remote_path is None:
            # 서버별 폴더 구조 적용: assets/서버명/파일명
            remote_path = f"assets/{self.server_prefix}/{filename}"

        try:
            print(f"[{self.server_prefix}] R2 uploading: {local_file_path} -> {remote_path}")
            self.s3_client.upload_file(local_file_path, self.bucket_name, remote_path)
            print(f"[OK] Upload complete!")
            return True
        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return False

    def sync_recommended_files(self):
        print(f"\n--- Gundammap R2 Auto Sync Start ({self.server_prefix}) ---")
        
        target_files = [
            "sasang_factory_results.txt",
            "vworld_ned.xml",
            "luLandDet.js",
            "luLandDetRelate.js"
        ]
        
        for file in target_files:
            if os.path.exists(file):
                self.upload_file(file)
            else:
                print(f"[SKIP] {file} (file not found locally)")

        print(f"--- R2 Auto Sync Complete ({self.server_prefix}) ---\n")

    def sync_static_files(self):
        print(f"\n--- Static Files Sync ({self.server_prefix}) ---")
        
        static_files = [
            ("static/css/map_app.css", f"{self.server_prefix}/static/css/map_app.css"),
            ("static/js/map_app.js", f"{self.server_prefix}/static/js/map_app.js")
        ]
        
        for local_path, remote_path in static_files:
            if os.path.exists(local_path):
                self.upload_file(local_path, remote_path)
            else:
                print(f"[SKIP] {local_path} (file not found locally)")
                
        print(f"--- Static Sync Complete ---\n")

if __name__ == "__main__":
    uploader = R2Uploader()
    if uploader.enabled:
        uploader.sync_recommended_files()
        uploader.sync_static_files()
    else:
        print("[INFO] Please add R2 credentials to .env file and run again.")
