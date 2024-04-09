from netmiko import ConnectHandler
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Router details
router = {
    'device_type': 'alcatel_sros',
    'host': '10.42.10.25',
    'username': 'AliDoski',
    'password': 'Al!$osk!22',
}

# Connect to the router and retrieve OSPF interface details
try:
    ssh_session = ConnectHandler(**router)
    # Send command and get output
    output = ssh_session.send_command("show router ospf interface detail")

    # Create a PDF file
    pdf_file = "ospf_interface_details.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Write original output to PDF
    lines = output.split("\n")
    y = 750  # Starting y-coordinate
    for line in lines:
        c.drawString(50, y, line)
        y -= 12  # Move to the next line
        if y < 50:
            c.showPage()  # Page break if y-coordinate reaches bottom
            y = 750  # Reset y-coordinate for new page

    # Extract information for each interface
    interface_info = {}
    interfaces = output.split("--------------------------------------------------------------")
    for interface in interfaces:
        if "Interface :" in interface:
            ospf_interface_info = {}
            lines = interface.split("\n")
            for line in lines:
                if "Admin Status" in line or "IP address" in line or "Area" in line \
                        or "cfg Metric" in line or "Auth Type" in line \
                        or "Hello Intrvl" in line or "Retrans Intrvl" in line or "Passive" in line:
                    key, value = map(str.strip, line.split(":", 1))
                    ospf_interface_info[key] = value
            interface_name = ospf_interface_info.get("Interface", "")
            interface_info[interface_name] = ospf_interface_info

    # Add a new page to the PDF for OSPF interface information
    c.showPage()

    # Write OSPF interface information to PDF
    y = 750  # Starting y-coordinate
    for interface_name, info in interface_info.items():
        c.drawString(50, y, f"Interface: {interface_name}")
        y -= 12
        for key, value in info.items():
            c.drawString(70, y, f"{key}: {value}")
            y -= 12

    # Save the PDF
    c.save()
    print(f"PDF generated successfully: {pdf_file}")

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the SSH session
    ssh_session.disconnect()
