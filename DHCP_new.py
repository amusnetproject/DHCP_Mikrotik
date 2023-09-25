from librouteros import connect

# Define API credentials for both routers
src_router_ip = '192.168.100.2'
src_router_username = 'admin'
src_router_password = 'admin'

dest_router_ip = '192.168.100.3'
dest_router_username = 'admin'
dest_router_password = 'admin'

try:
    # Connect to the source MikroTik router (from which you want to copy DHCP leases)
    src_router = connect(host=src_router_ip, username=src_router_username, password=src_router_password)

    # Connect to the destination MikroTik router (where you want to add DHCP leases)
    dest_router = connect(host=dest_router_ip, username=dest_router_username, password=dest_router_password)

    # Retrieve DHCP leases from the source router
    src_dhcp_leases = src_router(cmd='/ip/dhcp-server/lease/print')

    # Add DHCP leases to the destination router
    for lease in src_dhcp_leases:
        dest_router(cmd='/ip/dhcp-server/lease/add',
                    address=lease['address'],
                    mac_address=lease['mac-address'],
    print("DHCP leases copied successfully.")

except Exception as e:
    print(f"An error occurred: {str(e)}")

