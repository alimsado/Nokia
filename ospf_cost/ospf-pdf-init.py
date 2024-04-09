from netmiko import ConnectHandler
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

    # Create a PDF file
    pdf_file = "ospf_interface_details.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Write output to PDF
    lines = output.split("\n")
    y = 750  # Starting y-coordinate
    for line in lines:
        c.drawString(50, y, line)
        y -= 12  # Move to the next line

    # Save the PDF
    c.save()
    print(f"PDF generated successfully: {pdf_file}")

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the SSH session
    ssh_session.disconnect()
