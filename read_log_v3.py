try:
    # Read server_v3.log
    # Default encoding for redirection in Powershell is likely UTF-16 LE
    with open('server_v3.log', 'r', encoding='utf-16', errors='replace') as f:
        content = f.read()
        print(content[-3000:])
except Exception as e:
    print(f"Error reading utf-16: {e}")
    try:
        with open('server_v3.log', 'r', encoding='utf-8', errors='replace') as f:
            print(f.read()[-3000:])
    except Exception as e2:
        print(f"Error reading utf-8: {e2}")
