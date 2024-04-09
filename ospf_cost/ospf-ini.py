from netmiko import ConnectHandler

# Router details
router = {
    'device_type': 'alcatel_sros',
    'host': '10.42.10.39',
    'username': 'AliDoski',
    'password': 'Al!$osk!22',
}

# Connect to the router
try:
    ssh_session = ConnectHandler(**router)
    # Send command and get output
    output = ssh_session.send_command("show router ospf interface detail")
    print(output)

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the SSH session
    ssh_session.disconnect()
