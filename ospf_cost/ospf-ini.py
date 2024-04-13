from netmiko import ConnectHandler

# Router details
router = {
    'device_type': 'alcatel_sros',
    'host': '10.42.10.37',
    'username': 'AliDoski',
    'password': 'Al!$osk!22',
    'verbose': True  # Set verbose to True to increase debugging output

}

# Connect to the router
try:
    ssh_session = ConnectHandler(**router)
    # Send command and get output
    output = ssh_session.send_command("show router interface")
    print(output)

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the SSH session
    ssh_session.disconnect()
