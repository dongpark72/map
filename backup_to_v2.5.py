import shutil
import os
from datetime import datetime

# 백업할 파일 목록
files_to_backup = [
    'maps/models.py',
    'maps/views.py',
    'maps/urls.py',
    'templates/maps/map_app.html',
    'templates/maps/index.html',
    'docker-compose.yml',
    'gundammap/settings.py',
]

# 백업 디렉토리 생성
backup_dir = 'backups/v2.5'
os.makedirs(backup_dir, exist_ok=True)

# 타임스탬프
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

print(f"Creating backup v2.5 at {timestamp}...")
print(f"Backup directory: {backup_dir}\n")

backed_up = []
failed = []

for file_path in files_to_backup:
    try:
        if os.path.exists(file_path):
            # 백업 파일명 생성
            backup_path = os.path.join(backup_dir, file_path.replace('/', '_'))
            
            # 디렉토리 생성
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # 파일 복사
            shutil.copy2(file_path, backup_path)
            backed_up.append(file_path)
            print(f"[OK] Backed up: {file_path}")
        else:
            failed.append(f"{file_path} (not found)")
            print(f"[SKIP] Not found: {file_path}")
    except Exception as e:
        failed.append(f"{file_path} ({str(e)})")
        print(f"[ERROR] Failed: {file_path} - {e}")

# 백업 정보 파일 생성
info_file = os.path.join(backup_dir, 'backup_info.txt')
with open(info_file, 'w', encoding='utf-8') as f:
    f.write(f"Backup Version: v2.5\n")
    f.write(f"Timestamp: {timestamp}\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("=== Changes in v2.5 ===\n")
    f.write("1. Kamco (공매) Data Filtering:\n")
    f.write("   - Filter to show only real estate (land/buildings)\n")
    f.write("   - Exclude vehicles, securities, machinery\n")
    f.write("   - Parse GOODS_NM for missing area data\n")
    f.write("   - Use BID_MNMT_NO for bid count when BID_PRGN_NFT is empty\n\n")
    
    f.write("2. Auto-logout Feature:\n")
    f.write("   - Removed 10-minute inactivity auto-logout\n")
    f.write("   - Improved user convenience\n\n")
    
    f.write("3. Data Quality Improvements:\n")
    f.write("   - Land area (LAND_SQMS) with fallback parsing\n")
    f.write("   - Building area (BLD_SQMS) with fallback parsing\n")
    f.write("   - Bid count from BID_MNMT_NO field\n\n")
    
    f.write("4. Warehouse Data:\n")
    f.write("   - Confirmed CUSTODY_TARIFF_RT and BIZCOND_CUSTODY_ND_WAREHS_NM\n")
    f.write("   - Display '-' when data is not available from API\n\n")
    
    f.write(f"\n=== Backed up files ({len(backed_up)}) ===\n")
    for file in backed_up:
        f.write(f"  [OK] {file}\n")
    
    if failed:
        f.write(f"\n=== Failed files ({len(failed)}) ===\n")
        for file in failed:
            f.write(f"  [FAIL] {file}\n")

print(f"\n{'='*60}")
print(f"Backup completed!")
print(f"Total files backed up: {len(backed_up)}")
if failed:
    print(f"Failed: {len(failed)}")
print(f"Backup location: {os.path.abspath(backup_dir)}")
print(f"Info file: {os.path.abspath(info_file)}")
print(f"{'='*60}")
