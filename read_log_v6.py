import os

log_file = 'server_v6.log'
if os.path.exists(log_file):
    try:
        with open(log_file, 'r', encoding='utf-16', errors='replace') as f:
            print(f.read()[-2000:])
    except:
        try:
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                print(f.read()[-2000:])
        except Exception as e:
            print(f"Error: {e}")
else:
    print("Log file not found.")
