import re
from netmiko import ConnectHandler

# Router details
router = {
    'device_type': 'alcatel_sros',
    'host': '10.42.10.39',
    'username': 'AliDoski',
    'password': 'Al!$osk!22',
}

# Connect to the router and retrieve OSPF interface details
try:
    ssh_session = ConnectHandler(**router)
    # Send command and get output
    output = ssh_session.send_command("show router ospf interface detail")

    # Extract interface name and cfg Metric using regular expressions
    interfaces = re.split(r'(?=Interface : )', output)  # Split by Interface
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
