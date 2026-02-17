import paramiko

HOST = '175.126.187.59'
PORT = 22
USER = 'dongpark72'
PASS = 'timess9746'
REMOTE_PATH = '/volume1/docker/gundammap'

def main():
    output_lines = []
    
    def log(msg):
        print(msg)
        output_lines.append(msg)
    
    log("Connecting to server...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, PORT, USER, PASS)
    log("Connected!")
    
    # Check Docker containers
    log("\n=== Docker Containers ===")
    stdin, stdout, stderr = client.exec_command(
        f'echo {PASS} | sudo -S docker ps -a'
    )
    log(stdout.read().decode())
    
    # Check web container logs
    log("\n=== Web Container Logs (last 30 lines) ===")
    stdin, stdout, stderr = client.exec_command(
        f'echo {PASS} | sudo -S docker ps --format "{{{{.Names}}}}" | grep -i web'
    )
    web_container = stdout.read().decode().strip()
    log(f"Web container: {web_container}")
    
    if web_container:
        stdin, stdout, stderr = client.exec_command(
            f'echo {PASS} | sudo -S docker logs --tail 30 {web_container}'
        )
        logs = stdout.read().decode()
        err_logs = stderr.read().decode()
        log(logs)
        if err_logs:
            log("STDERR:")
            log(err_logs)
    
    # Test localhost connection from server
    log("\n=== Testing localhost:8000 ===")
    stdin, stdout, stderr = client.exec_command(
        'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000'
    )
    http_code = stdout.read().decode().strip()
    log(f"HTTP Status Code: {http_code}")
    
    client.close()
    log("\nDone!")
    
    # Save to file
    with open('server_status_output.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    print("\nOutput saved to server_status_output.txt")

if __name__ == "__main__":
    main()
