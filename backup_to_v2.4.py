import os
import shutil
import logging

# Configuration
SOURCE_DIR = r"e:\Antigravity\Gundammap"
DEST_DIR = r"e:\Antigravity\Gundammap\backups\v2.4"
EXCLUDE_DIRS = {
    'backups', '.git', '__pycache__', '.idea', '.vscode', 'venv', 'node_modules', 
    'static', 'media', 'staticfiles'
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BackupV2.4")

def backup_project():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        logger.info(f"Created destination directory: {DEST_DIR}")

    logger.info(f"Starting backup from {SOURCE_DIR} to {DEST_DIR}")

    file_count = 0
    dir_count = 0

    for root, dirs, files in os.walk(SOURCE_DIR):
        # Modify dirs in-place to filter out excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        # Calculate relative path to mirror structure
        rel_path = os.path.relpath(root, SOURCE_DIR)
        
        if rel_path == ".":
            dest_root = DEST_DIR
        else:
            dest_root = os.path.join(DEST_DIR, rel_path)
            if not os.path.exists(dest_root):
                os.makedirs(dest_root)
                dir_count += 1

        for file in files:
            # Skip the backup script itself if it's running
            if file == "backup_to_v2.4.py":
                continue
                
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)

            try:
                shutil.copy2(src_file, dest_file)
                file_count += 1
                if file_count % 50 == 0:
                    logger.info(f"Copied {file_count} files... (Last: {file})")
            except Exception as e:
                logger.error(f"Failed to copy {src_file}: {e}")

    logger.info(f"Backup completed. Total {dir_count} directories and {file_count} files copied.")
    
    # Verification of critical files
    critical_files = [
        r"templates\maps\map_app.html",
        r"maps\views.py",
        r"maps\urls.py",
        r"manage.py",
        r".env"
    ]
    
    logger.info("=== Verifying Critical Files ===")
    all_critical_present = True
    for crit in critical_files:
        path = os.path.join(DEST_DIR, crit)
        if os.path.exists(path):
            size = os.path.getsize(path)
            logger.info(f"[OK] {crit} exists ({size} bytes)")
        else:
            logger.error(f"[MISSING] {crit} not found in backup!")
            all_critical_present = False
            
    if all_critical_present:
        print("SUCCESS: Full backup to v2.4 completed successfully.")
    else:
        print("WARNING: Backup completed but some critical files are missing.")

if __name__ == "__main__":
    backup_project()
