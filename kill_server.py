import os
import subprocess
import time

print("Checking port 8000...")
try:
    # Find PID using port 8000
    # Use netstat
    res = subprocess.run("netstat -ano | findstr :8000", shell=True, capture_output=True, text=True)
    if res.stdout:
        lines = res.stdout.strip().split('\n')
        pids = set()
        for line in lines:
            if 'LISTENING' in line:
                parts = line.strip().split()
                if len(parts) > 0:
                    pid = parts[-1]
                    if pid.isdigit() and pid != '0':
                        pids.add(pid)
        
        if pids:
            print(f"Found processes on port 8000: {pids}")
            for pid in pids:
                print(f"Killing PID {pid}...")
                os.system(f"taskkill /F /PID {pid}")
            print("Killed all.")
        else:
            print("No LISTENING process found on 8000.")
    else:
        print("Port 8000 is free.")

except Exception as e:
    print(f"Error: {e}")
