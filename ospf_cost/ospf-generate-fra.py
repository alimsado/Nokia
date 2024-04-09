import re
from netmiko import ConnectHandler
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Router details
router = {
    'device_type': 'alcatel_sros',
    'host': '10.42.10.41',
    'username': 'AliDoski',
    'password': 'Al!$osk!22',
}

# Connect to the router and retrieve OSPF interface details
try:
    ssh_session = ConnectHandler(**router)
    
    # Retrieve system information
    system_info_output = ssh_session.send_command("show system information")
    match = re.search(r'System Name\s*:\s*(.+)', system_info_output)
    if match:
        router_name = match.group(1).strip()
    else:
        router_name = "Unknown"

    # Send command to get OSPF interface details
    ospf_output = ssh_session.send_command("show router ospf interface detail")

    # Extract interface name and cfg Metric using regular expressions
    interfaces = re.split(r'(?=-{80,})', ospf_output)  # Split by a line of 80 or more hyphens

    # Extract interface names and cfg Metric
    data = [["Router Name", "Interface Name", "OSPF cfg Metric"]]
    for interface in interfaces:
        match = re.search(r'Interface : (.+)', interface)
        if match:
            interface_name = match.group(1).strip()
            cfg_metric_match = re.search(r'Cfg Metric\s*:\s*(\d+)', interface)
            if cfg_metric_match:
                cfg_metric = cfg_metric_match.group(1).strip()
                data.append([router_name, interface_name, cfg_metric])

    # Create a PDF file
    pdf_file = "ospf_interface_details.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    
    # Create table
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    # Add table to the PDF
    doc.build([table])

    print(f"PDF generated successfully: {pdf_file}")

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the SSH session
    ssh_session.disconnect()