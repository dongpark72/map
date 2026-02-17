try:
    with open('server.log', 'r', encoding='utf-8', errors='replace') as f:
        # Read lines and print the last 100 lines
        lines = f.readlines()
        print("".join(lines[-100:]))
except Exception as e:
    print(f"Error reading log: {e}")
