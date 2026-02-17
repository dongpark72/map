import paramiko
import sys

HOST = '175.126.187.59'
USER = 'dongpark72'
PASS = 'timess9746'

def test_connection():
    output_lines = []
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS)
        
        output_lines.append("="*70)
        output_lines.append("Server Connection Test Results")
        output_lines.append("="*70)
        
        # Test 1: Container status
        output_lines.append("\n1. Container Status:")
        stdin, stdout, stderr = client.exec_command(
            f'cd /volume1/docker/gundammap && echo {PASS} | sudo -S /usr/local/bin/docker-compose ps'
        )
        output_lines.append(stdout.read().decode())
        
        # Test 2: Port check
        output_lines.append("\n2. Port 8000 Status:")
        stdin, stdout, stderr = client.exec_command(
            f'echo {PASS} | sudo -S netstat -tlnp | grep :8000'
        )
        port_output = stdout.read().decode()
        if port_output:
            output_lines.append("Port 8000 is LISTENING")
            output_lines.append(port_output)
        else:
            output_lines.append("Port 8000 is NOT listening")
        
        # Test 3: Container logs
        output_lines.append("\n3. Web Container Logs (last 30 lines):")
        stdin, stdout, stderr = client.exec_command(
            f'echo {PASS} | sudo -S /usr/local/bin/docker ps --format "{{{{.Names}}}}" | grep web'
        )
        container = stdout.read().decode().strip()
        
        if container:
            output_lines.append(f"Container name: {container}")
            stdin, stdout, stderr = client.exec_command(
                f'echo {PASS} | sudo -S /usr/local/bin/docker logs --tail 30 {container}'
            )
            output_lines.append(stdout.read().decode())
            err = stderr.read().decode()
            if err:
                output_lines.append("\nError logs:")
                output_lines.append(err)
        
        # Test 4: Curl test
        output_lines.append("\n4. Local Connection Test:")
        stdin, stdout, stderr = client.exec_command(
            'curl -I http://localhost:8000 2>&1 | head -10'
        )
        output_lines.append(stdout.read().decode())
        
        output_lines.append("\n" + "="*70)
        output_lines.append("Test Complete")
        output_lines.append("="*70)
        
        client.close()
        
    except Exception as e:
        output_lines.append(f"\nError: {e}")
        import traceback
        output_lines.append(traceback.format_exc())
    
    # Write to file
    result = "\n".join(output_lines)
    with open('connection_test_result.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(result)
    print("\n\nResults saved to: connection_test_result.txt")

if __name__ == "__main__":
    test_connection()
