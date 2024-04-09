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

    # Write output to PDF
    lines = output.split("\n")
    y = 750  # Starting y-coordinate
    cfg_metric_dict = {}  # Dictionary to store cfg Metric for each interface
    for line in lines:
        if "Interface :" in line:
            interface_name = line.split(":")[1].strip()
        elif "cfg Metric" in line:
            cfg_metric = line.split(":")[1].strip()
            cfg_metric_dict[interface_name] = cfg_metric
        c.drawString(50, y, line)
        y -= 12  # Move to the next line
        if y < 50:
            c.showPage()  # Page break if y-coordinate reaches bottom
            y = 750  # Reset y-coordinate for new page

    # Add cfg Metric for each interface to the next page
    c.showPage()
    y = 750  # Starting y-coordinate for the next page
    for interface_name, cfg_metric in cfg_metric_dict.items():
        c.drawString(50, y, f"Interface: {interface_name}, cfg Metric: {cfg_metric}")
        y -= 12  # Move to the next line

    # Save the PDF
    c.save()
    print(f"PDF generated successfully: {pdf_file}")

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the SSH session
    ssh_session.disconnect()
