#!/usr/bin/env python3
"""
🚀 R2 CDN 자동 적용 스크립트
이 스크립트는 .agent-cdn-setup-guide.md의 모든 단계를 자동으로 수행합니다.

사용법:
    python apply_cdn_auto.py

작동 방식:
    1. .env 파일에서 R2 설정 확인
    2. requirements.txt에 필수 패키지 추가
    3. settings.py에 R2 CDN 설정 추가
    4. 템플릿 파일에 {% load static %} 추가
    5. R2에 정적 파일 업로드
    6. 검증 스크립트 실행
"""

import os
import re
import sys
from pathlib import Path


class CDNAutoApplier:
    def __init__(self, project_root=None):
        self.project_root = Path(project_root or os.getcwd())
        self.env_file = self.project_root / ".env"
        self.requirements_file = self.project_root / "requirements.txt"
        self.errors = []
        self.warnings = []
        
    def log_error(self, msg):
        self.errors.append(msg)
        print(f"[ERROR] {msg}")
        
    def log_warning(self, msg):
        self.warnings.append(msg)
        print(f"[WARNING] {msg}")
        
    def log_success(self, msg):
        print(f"[OK] {msg}")
        
    def log_info(self, msg):
        print(f"[INFO] {msg}")
        
    # ========================================
    # Step 1: .env 파일 검증
    # ========================================
    def verify_env_file(self):
        print("\n" + "="*80)
        print("Step 1: .env 파일 검증")
        print("="*80)
        
        if not self.env_file.exists():
            self.log_error(f".env 파일이 없습니다: {self.env_file}")
            return False
            
        with open(self.env_file, 'r', encoding='utf-8') as f:
            env_content = f.read()
            
        required_keys = [
            'R2_ACCESS_KEY_ID',
            'R2_SECRET_ACCESS_KEY',
            'R2_BUCKET_NAME',
            'R2_ACCOUNT_ID',
            'R2_ENDPOINT_URL',
            'R2_SERVER_PREFIX',
            'R2_CUSTOM_DOMAIN'
        ]
        
        missing_keys = []
        for key in required_keys:
            if f"{key}=" not in env_content:
                missing_keys.append(key)
                
        if missing_keys:
            self.log_error(f".env 파일에 다음 항목이 없습니다: {', '.join(missing_keys)}")
            return False
            
        self.log_success(".env 파일에 모든 R2 설정이 있습니다")
        return True
        
    # ========================================
    # Step 2: requirements.txt 업데이트
    # ========================================
    def update_requirements(self):
        print("\n" + "="*80)
        print("Step 2: requirements.txt 업데이트")
        print("="*80)
        
        required_packages = [
            "boto3>=1.34.0",
            "django-storages[s3]>=1.14.0"
        ]
        
        if not self.requirements_file.exists():
            self.log_warning(f"requirements.txt가 없습니다. 새로 생성합니다.")
            with open(self.requirements_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(required_packages) + "\n")
            self.log_success("requirements.txt 생성 완료")
            return True
            
        with open(self.requirements_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        needs_update = False
        for package in required_packages:
            package_name = package.split('>=')[0].split('[')[0]
            if package_name not in content:
                self.log_info(f"추가 필요: {package}")
                content += f"\n{package}"
                needs_update = True
                
        if needs_update:
            with open(self.requirements_file, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log_success("requirements.txt 업데이트 완료")
        else:
            self.log_success("requirements.txt에 필수 패키지가 모두 있습니다")
            
        return True
        
    # ========================================
    # Step 3: settings.py 찾기 및 업데이트
    # ========================================
    def find_settings_file(self):
        """Django settings.py 파일 찾기"""
        # 일반적인 Django 프로젝트 구조에서 settings.py 찾기
        possible_locations = [
            self.project_root / "settings.py",
            self.project_root / "config" / "settings.py",
        ]
        
        # 프로젝트 이름으로 된 폴더에서 찾기
        for item in self.project_root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                settings_path = item / "settings.py"
                if settings_path.exists():
                    return settings_path
                    
        for path in possible_locations:
            if path.exists():
                return path
                
        return None
        
    def update_settings(self):
        print("\n" + "="*80)
        print("Step 3: settings.py 업데이트")
        print("="*80)
        
        settings_file = self.find_settings_file()
        if not settings_file:
            self.log_error("settings.py 파일을 찾을 수 없습니다")
            return False
            
        self.log_info(f"settings.py 위치: {settings_file}")
        
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 이미 R2 설정이 있는지 확인
        if "R2_CUSTOM_DOMAIN" in content and "S3Boto3Storage" in content:
            self.log_success("settings.py에 이미 R2 CDN 설정이 있습니다")
            return True
            
        # R2 설정 코드 추가
        r2_config = '''
# ============================================================
# Cloudflare R2 CDN Configuration (Auto-generated)
# ============================================================
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
R2_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL')
R2_SERVER_PREFIX = os.getenv('R2_SERVER_PREFIX', 'dev')

if R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY:
    # Use R2 for static files
    AWS_ACCESS_KEY_ID = R2_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = R2_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = R2_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = R2_ENDPOINT_URL
    AWS_S3_REGION_NAME = 'auto'
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_QUERYSTRING_AUTH = False
    
    # Static files location in R2
    AWS_LOCATION = f'{R2_SERVER_PREFIX}/static'
    
    # Custom Domain for CDN
    R2_CUSTOM_DOMAIN = os.getenv('R2_CUSTOM_DOMAIN')
    if R2_CUSTOM_DOMAIN:
        # Update STATIC_URL to use CDN
        domain = R2_CUSTOM_DOMAIN.replace('https://', '').replace('http://', '').strip('/')
        AWS_S3_CUSTOM_DOMAIN = domain
        # Set STATIC_URL to CDN domain + location path
        STATIC_URL = f'https://{domain}/{AWS_LOCATION}/'
    else:
        # Fallback to R2 endpoint if no custom domain
        STATIC_URL = f'{R2_ENDPOINT_URL}/{R2_BUCKET_NAME}/{AWS_LOCATION}/'
    
    # IMPORTANT: Use S3Boto3Storage for both (NOT S3StaticStorage)
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
    }
'''
        
        # STATIC_URL 설정 찾아서 주석 처리
        content = re.sub(
            r'^(STATIC_URL\s*=.*)$',
            r'# \1  # Replaced by R2 CDN config below',
            content,
            flags=re.MULTILINE
        )
        
        # 파일 끝에 R2 설정 추가
        content += "\n" + r2_config
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        self.log_success("settings.py에 R2 CDN 설정 추가 완료")
        return True
        
    # ========================================
    # Step 4: 템플릿 파일 업데이트
    # ========================================
    def update_templates(self):
        print("\n" + "="*80)
        print("Step 4: 템플릿 파일 업데이트")
        print("="*80)
        
        templates_dir = self.project_root / "templates"
        if not templates_dir.exists():
            self.log_warning("templates 폴더가 없습니다")
            return True
            
        html_files = list(templates_dir.rglob("*.html"))
        if not html_files:
            self.log_warning("HTML 템플릿 파일이 없습니다")
            return True
            
        updated_count = 0
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 이미 {% load static %}이 있는지 확인
            if "{% load static %}" in content:
                continue
                
            # DOCTYPE 또는 <html> 태그 앞에 {% load static %} 추가
            if "<!DOCTYPE" in content or "<html" in content:
                content = "{% load static %}\n" + content
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                self.log_info(f"업데이트: {html_file.name}")
                
        if updated_count > 0:
            self.log_success(f"{updated_count}개 템플릿 파일 업데이트 완료")
        else:
            self.log_success("모든 템플릿 파일에 이미 {% load static %}이 있습니다")
            
        return True
        
    # ========================================
    # Step 5: R2 업로드 스크립트 생성
    # ========================================
    def create_r2_sync_script(self):
        print("\n" + "="*80)
        print("Step 5: R2 업로드 스크립트 생성")
        print("="*80)
        
        r2_sync_file = self.project_root / "r2_sync_tool.py"
        
        if r2_sync_file.exists():
            self.log_success("r2_sync_tool.py가 이미 있습니다")
            return True
            
        r2_sync_code = '''import os
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
            remote_path = f"assets/{self.server_prefix}/{filename}"

        try:
            print(f"[{self.server_prefix}] R2 uploading: {local_file_path} -> {remote_path}")
            self.s3_client.upload_file(local_file_path, self.bucket_name, remote_path)
            print(f"[OK] Upload complete!")
            return True
        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return False

    def sync_static_files(self):
        print(f"\\n--- Static Files Sync ({self.server_prefix}) ---")
        
        # static 폴더에서 모든 CSS, JS 파일 찾기
        static_dir = "static"
        uploaded = 0
        
        if os.path.exists(static_dir):
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    if file.endswith(('.css', '.js', '.png', '.jpg', '.svg', '.ico')):
                        local_path = os.path.join(root, file)
                        # static/ 이후 경로 추출
                        relative_path = os.path.relpath(local_path, ".")
                        remote_path = f"{self.server_prefix}/{relative_path}".replace("\\\\", "/")
                        
                        if self.upload_file(local_path, remote_path):
                            uploaded += 1
        else:
            print(f"[SKIP] {static_dir} folder not found")
                
        print(f"--- Static Sync Complete ({uploaded} files uploaded) ---\\n")

if __name__ == "__main__":
    uploader = R2Uploader()
    if uploader.enabled:
        uploader.sync_static_files()
    else:
        print("[INFO] Please add R2 credentials to .env file and run again.")
'''
        
        with open(r2_sync_file, 'w', encoding='utf-8') as f:
            f.write(r2_sync_code)
            
        self.log_success("r2_sync_tool.py 생성 완료")
        return True
        
    # ========================================
    # Step 6: 검증 스크립트 생성
    # ========================================
    def create_verify_script(self):
        print("\n" + "="*80)
        print("Step 6: 검증 스크립트 생성")
        print("="*80)
        
        verify_file = self.project_root / "verify_cdn.py"
        
        verify_code = '''import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

def verify_cdn(url, cdn_domain):
    try:
        r = requests.get(url, timeout=10)
        print(f"Status Code: {r.status_code}")
        
        if r.status_code != 200:
            print(f"❌ Error: HTTP {r.status_code}")
            return False
        
        # CDN 도메인 확인
        has_cdn = cdn_domain in r.text
        print(f"\\n{'✅' if has_cdn else '❌'} CDN domain ({cdn_domain}) found: {has_cdn}")
        
        # CSS/JS 파일 찾기
        css_matches = re.findall(r'href=["\\']([^\\"\\']+ \\.css[^\\"\\']*)["\\']', r.text)
        js_matches = re.findall(r'src=["\\']([^\\"\\']+ \\.js[^\\"\\']*)["\\']', r.text)
        
        print(f"\\nCSS Files ({len(css_matches)}):")
        for url in css_matches:
            cdn_marker = " [CDN]" if cdn_domain in url else ""
            print(f"  - {url}{cdn_marker}")
        
        print(f"\\nJS Files ({len(js_matches)}):")
        for url in js_matches:
            cdn_marker = " [CDN]" if cdn_domain in url else ""
            print(f"  - {url}{cdn_marker}")
        
        # 요약
        all_static = css_matches + js_matches
        cdn_count = sum(1 for url in all_static if cdn_domain in url)
        
        print(f"\\n{'='*80}")
        print(f"Total static files: {len(all_static)}")
        print(f"Using CDN: {cdn_count}")
        print(f"CDN Status: {'✅ ENABLED' if cdn_count > 0 else '❌ NOT ENABLED'}")
        
        return cdn_count > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # .env에서 설정 읽기
    cdn_domain = os.getenv('R2_CUSTOM_DOMAIN', 'assets.goal-runner.com')
    cdn_domain = cdn_domain.replace('https://', '').replace('http://', '')
    
    # 사용자에게 URL 입력 요청
    url = input("검증할 웹사이트 URL을 입력하세요 (예: https://map.goal-runner.com/portal/): ").strip()
    
    if url:
        verify_cdn(url, cdn_domain)
    else:
        print("❌ URL을 입력해주세요")
'''
        
        with open(verify_file, 'w', encoding='utf-8') as f:
            f.write(verify_code)
            
        self.log_success("verify_cdn.py 생성 완료")
        return True
        
    # ========================================
    # 메인 실행
    # ========================================
    def run(self):
        print("\n" + "="*80)
        print("R2 CDN Auto-Apply Starting...")
        print("="*80)
        print(f"Project Path: {self.project_root}")
        
        steps = [
            ("1. .env file verification", self.verify_env_file),
            ("2. requirements.txt update", self.update_requirements),
            ("3. settings.py update", self.update_settings),
            ("4. template files update", self.update_templates),
            ("5. R2 upload script creation", self.create_r2_sync_script),
            ("6. verification script creation", self.create_verify_script),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n[FAILED] {step_name}")
                break
        else:
            print("\n" + "="*80)
            print("[SUCCESS] All steps completed!")
            print("="*80)
            print("\nNext steps:")
            print("1. python r2_sync_tool.py  # Upload static files to R2")
            print("2. Deploy to server (run deploy script)")
            print("3. python verify_cdn.py    # Verify CDN is working")
            return True
            
        if self.errors:
            print("\n" + "="*80)
            print("[ERRORS]:")
            for error in self.errors:
                print(f"  - {error}")
                
        if self.warnings:
            print("\n[WARNINGS]:")
            for warning in self.warnings:
                print(f"  - {warning}")
                
        return False


if __name__ == "__main__":
    applier = CDNAutoApplier()
    success = applier.run()
    sys.exit(0 if success else 1)
