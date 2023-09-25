import paramiko

# MikroTik Router SSH information
router_ip = '192.168.100.2'
router_username = 'admin'
router_password = 'admin'
output_file = 'dhcp_leases.txt'

# SSH connection setup
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(router_ip, username=router_username, password=router_password, timeout=10)

    # Run the command to show DHCP leases
    command = '/ip dhcp-server lease print'
    stdin, stdout, stderr = ssh.exec_command(command)

    # Read the output
    dhcp_leases = stdout.read().decode()

    # Write the output to a file
    with open(output_file, 'w') as f:
        f.write(dhcp_leases)

    print(f"DHCP leases saved to {output_file}")

except paramiko.AuthenticationException:
    print("Authentication failed. Please check your username and password.")
except paramiko.SSHException as e:
    print(f"SSH connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    ssh.close()

