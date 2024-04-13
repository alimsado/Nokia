from netmiko import ConnectHandler

# Router details
router = {
    'device_type': 'alcatel_sros',
    'host': '10.42.10.37',
    'username': 'AliDoski',
    'password': 'Al!$osk!22',
}

# Connect to the router
try:
    print("Connecting to the router...")
    ssh_session = ConnectHandler(**router)
    print("Connection successful.")

    # Send command and get output
    print("Sending command 'show system information'...")
    output = ssh_session.send_command("show system information")
    print("Command executed successfully.")

    # Print command output
    print("Command output:")
    print(output)

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the SSH session
    print("Closing SSH session...")
    ssh_session.disconnect()
    print("SSH session closed.")
