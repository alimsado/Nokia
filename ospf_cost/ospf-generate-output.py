import re
from netmiko import ConnectHandler

# Router details
router = {
    'device_type': 'alcatel_sros',
    'host': '10.42.10.37',
    'username': 'AliDoski',
    'password': 'Al!$osk!22',
}

# Connect to the router and retrieve OSPF interface details
try:
    ssh_session = ConnectHandler(**router)
    
    # Send command to get OSPF interface details
    ospf_output = ssh_session.send_command("show router ospf interface detail")

    # Extract interface name and cfg Metric using regular expressions
    interfaces = re.split(r'(?=Interface : )', ospf_output)  # Split by Interface
    
    # Retrieve system information
    system_info_output = ssh_session.send_command("show system information")
    system_name_match = re.search(r'System Name\s*:\s*(.+)', system_info_output)
    if system_name_match:
        system_name = system_name_match.group(1).strip()
    else:
        system_name = "Unknown"

    print(f"System Name: {system_name}")

    for interface in interfaces:
        match = re.search(r'Interface : (.+)', interface)
        if match:
            interface_name = match.group(1)
            cfg_metric_match = re.search(r'Cfg Metric\s*:\s*(\d+)', interface)
            if cfg_metric_match:
                cfg_metric = cfg_metric_match.group(1)
                print(f"Interface: {interface_name.strip()}, cfg Metric: {cfg_metric.strip()}")

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the SSH session
    ssh_session.disconnect()
