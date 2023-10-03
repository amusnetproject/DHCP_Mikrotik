import subprocess
import paramiko  # Import the paramiko library for SSH communication

# Define router information with SSH credentials
router_info = [
    {'ip': '192.168.100.2', 'username': 'admin', 'password': 'admin'},
    {'ip': '192.168.100.3', 'username': 'admin', 'password': 'admin'},
]

output_file = 'dhcp_leases_VRRP_master.txt'

# Define the command to execute to fetch VRRP status
vrrp_command = "/interface vrrp print"
#dhcp_command = "/ip dhcp-server lease print"

# Establish SSH connections to the routers
ssh_clients = []

def establish_ssh_connection(router_info):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(router_info['ip'], username=router_info['username'], password=router_info['password'])
        return ssh
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {router_info['ip']}")
    except paramiko.SSHException as e:
        print(f"SSH error for {router_info['ip']}: {str(e)}")
    except Exception as e:
        print(f"An error occurred for {router_info['ip']}: {str(e)}")
    return None


# Connect to each router and store SSH clients
for router in router_info:
    ssh = establish_ssh_connection(router)
    if ssh:
        print(f"Connected to {router['ip']}")
        ssh_clients.append({'info': router, 'ssh': ssh})

# Find the VRRP master router by searching for "RW" in the stdout of the vrrp_command
vrrp_master_info = None
vrrp_master_keyword= "RM"

for client in ssh_clients:
    ssh = client['ssh']

    try:
        # Run the command and capture the stdout as text
        result = ssh.exec_command(vrrp_command)
        stdout_text = result[1].read().decode('utf-8')
        rm_check = stdout_text.split()
        for each in rm_check:
         if each == vrrp_master_keyword:
           vrrp_master_info = client['info']
           break
          
    except Exception as e:
        print(f"Error executing the command on {client['info']['ip']}: {str(e)}")

# Check if a VRRP master router was found
if vrrp_master_info:
    print(f"{vrrp_master_info['ip']} is the VRRP master.")
else:
    print("No VRRP master router found.")
    
try:
    ssh.connect(vrrp_master_info['ip'],username=vrrp_master_info['username'],password=vrrp_master_info['password'])

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

# Close all SSH connections
for client in ssh_clients:
    ssh = client['ssh']
    ssh.close()

