import re
from netmiko import ConnectHandler

# Function to read router details from igws.txt file
def read_router_details(file_path):
    routers = []
    with open(file_path, 'r') as file:
        for line in file:
            ip, system_name = line.strip().split()
            routers.append({'ip': ip, 'system_name': system_name})
    return routers

# Connect to each router and retrieve OSPF interface details
try:
    # Read router details from igws.txt file
    routers = read_router_details('igws.txt')

    for router in routers:
        # Router details
        router_details = {
            'device_type': 'alcatel_sros',
            'host': router['ip'],
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        }

        print(f"Connecting to router {router['ip']} ({router['system_name']})...")

        # Connect to the router
        ssh_session = ConnectHandler(**router_details)
        
        # Send command to get OSPF interface details
        ospf_output = ssh_session.send_command("show router ospf interface detail")

        # Extract interface name and cfg Metric using regular expressions
        interfaces = re.split(r'(?=Interface : )', ospf_output)  # Split by Interface

        print(f"System Name: {router['system_name']}")

        for interface in interfaces:
            match = re.search(r'Interface : (.+)', interface)
            if match:
                interface_name = match.group(1)
                cfg_metric_match = re.search(r'Cfg Metric\s*:\s*(\d+)', interface)
                if cfg_metric_match:
                    cfg_metric = cfg_metric_match.group(1)
                    print(f"Interface: {interface_name.strip()}, cfg Metric: {cfg_metric.strip()}")

        # Close the SSH session
        ssh_session.disconnect()

except Exception as e:
    print("An error occurred:", str(e))
