# Gundam Map Deployment Guide for Synology NAS

This project is a GeoDjango application designed to be deployed on Synology NAS using Docker. It supports Google Maps, Kakao Maps, and Naver Maps with Cadastral (지적도) layers.

## 🚀 Quick Start

### Current Deployment Status
- **Server**: 175.126.187.59:8000
- **Status**: ✅ Running
- **Last Updated**: 2026-01-02

## Prerequisites

1.  **Synology NAS** with **Container Manager** (formerly Docker) installed.
2.  **Web Station** (optional, if you want to reverse proxy) or just use the mapped port.
3.  **SSH Access** enabled on your NAS (for initial setup if needed) or use Portainer/Synology GUI.
4.  API Keys for:
    *   Google Maps JavaScript API
    *   Kakao Maps JavaScript API
    *   Naver Maps (NCP) Client ID
    *   VWorld API Key

## Installation Steps

### 1. File Transfer
Ensure all files in this directory are uploaded to your NAS.
*   Recommended Path: `/volume1/docker/gundammap/`
*   Since you are likely accessing this via SMB/SFTP, simply copy the files to the mapped drive.

### 2. Environment Configuration
Edit the `.env` file in the project root:

```env
DEBUG=1
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=*

# Database
DB_NAME=gundammap
DB_USER=postgres
DB_PASSWORD=your-password-here
DB_HOST=db
DB_PORT=5432

# Map API Keys
GOOGLE_MAPS_API_KEY=your_key_here
KAKAO_MAPS_API_KEY=your_key_here
NAVER_MAPS_CLIENT_ID=your_id_here
VWORLD_API_KEY=your_key_here
```

**Important**: Make sure `DB_USER=postgres` (not `dongpark` or other custom users)

### 3. Deploy with Docker Compose

**Option A: Using Synology Container Manager (GUI)**
1.  Open Container Manager.
2.  Go to **Project** -> **Create**.
3.  Name: `gundammap`.
4.  Path: Select the folder where you uploaded the files (e.g., `/docker/gundammap`).
5.  Select "Use existing docker-compose.yml".
6.  Click **Next** and **Done**. The project will build and start.

**Option B: Using SSH (Command Line)**
1.  SSH into your NAS.
2.  Navigate to the directory: `cd /volume1/docker/gundammap`
3.  Run: `sudo docker-compose up -d --build`

**Option C: Using Deployment Scripts (Recommended)**
From your local machine:
```bash
# Full deployment
python nas_deploy.py

# Fix and restart server
python fix_server.py

# Just restart containers
python restart_containers.py
```

### 4. Access the Site
Open your browser and navigate to:
`http://<NAS_IP_ADDRESS>:8000`

Example: `http://175.126.187.59:8000`

## 🛠️ Utility Scripts

### Server Management
- **`diagnose_server.py`** - Comprehensive server diagnostics
- **`fix_server.py`** - Complete server rebuild and restart
- **`restart_containers.py`** - Quick container restart
- **`fix_database.py`** - Fix database authentication issues

### Testing & Monitoring
- **`test_connection.py`** - Test server connectivity
- **`test_and_save.py`** - Test and save results to file
- **`quick_status.py`** - Quick status check

### Deployment
- **`nas_deploy.py`** - Deploy all files to NAS
- **`upload_compose.py`** - Upload docker-compose.yml and restart

### Usage Example
```bash
# Check server status
python test_and_save.py

# View results
cat connection_test_result.txt

# Restart if needed
python restart_containers.py
```

## 🔧 Troubleshooting

### "페이지에 연결할 수 없습니다" Error
1. Check container status: `python test_and_save.py`
2. Restart containers: `python restart_containers.py`
3. Check logs in `connection_test_result.txt`

### Database Connection Errors
If you see "password authentication failed":
1. Ensure `.env` has `DB_USER=postgres`
2. Run: `python fix_database.py`

### Port 8000 Not Accessible from Outside
1. Check NAS firewall: Control Panel > Security > Firewall
2. Add rule to allow port 8000
3. Or use reverse proxy: Control Panel > Application Portal > Reverse Proxy

## Real-time Code Updates
This project is configured with a volume mount in `docker-compose.yml`:
```yaml
volumes:
  - .:/app
```
This means any change you make to the files in the `gundammap` folder (via SMB or SFTP) will be immediately reflected in the container.
*   **Python Code**: Django's runserver will auto-reload when python files change.
*   **Templates/HTML**: Changes are reflected on page refresh.

## Database
A PostGIS database is automatically created running on port 5432 (internal). Data is persisted in the `postgres_data` volume.

## 📊 Architecture

```
┌─────────────────────────────────────┐
│   Browser (Port 8000)               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Docker Network (gundammap-network)│
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │ Web Container│  │ DB Container│ │
│  │ (Django)     │──│ (PostgreSQL)│ │
│  │ Port 8000    │  │ Port 5432   │ │
│  └──────────────┘  └─────────────┘ │
└─────────────────────────────────────┘
```

## 📝 Recent Updates

### 2026-01-02
- ✅ Fixed database authentication issue
- ✅ Updated docker-compose.yml with restart policies
- ✅ Added network configuration
- ✅ Created utility scripts for easier management
- ✅ Server is now running successfully

For detailed information, see `SERVER_FIX_REPORT.md`

## ⚠️ Production Notes

**Current Setup**: Development mode with Django's built-in server

**For Production**, consider:
1. Set `DEBUG=0` in `.env`
2. Use Gunicorn instead of `runserver`
3. Add Nginx reverse proxy
4. Configure proper ALLOWED_HOSTS
5. Use HTTPS with SSL certificates

## 📞 Support

If you encounter issues:
1. Run diagnostics: `python diagnose_server.py`
2. Check logs: `python test_and_save.py`
3. Review `SERVER_FIX_REPORT.md` for common issues

