try:
    # Powershell '>' creates UTF-16 LE file
    with open('server_v2.log', 'r', encoding='utf-16', errors='replace') as f:
        content = f.read()
        print(content[-2000:]) # Read last 2000 chars
except Exception as e:
    print(f"Error reading log: {e}")
    # Fallback to utf-8 just in case
    try:
        with open('server_v2.log', 'r', encoding='utf-8', errors='replace') as f:
            print(f.read()[-2000:])
    except:
        pass
