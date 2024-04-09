import re
from netmiko import ConnectHandler
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def get_router_info(router_details):
    try:
        # Connect to the router
        ssh_session = ConnectHandler(**router_details)
        
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
        interfaces = re.split(r'(?=Interface : )', ospf_output)  # Split by Interface

        # Extract interface names and cfg Metric
        data = []
        first_row = True
        for interface in interfaces:
            match = re.search(r'Interface : (.+)', interface)
            if match:
                interface_name = match.group(1).strip()
                cfg_metric_match = re.search(r'Cfg Metric\s*:\s*(\d+)', interface)
                if cfg_metric_match:
                    cfg_metric = cfg_metric_match.group(1).strip()
                    if first_row:
                        data.append([router_name, interface_name, cfg_metric])
                        first_row = False
                    else:
                        data.append(["", interface_name, cfg_metric])

        return data

    except Exception as e:
        print(f"An error occurred while connecting to {router_details['host']}: {str(e)}")
        return None

def generate_pdf(data, pdf_file):
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

def main():
    routers = [
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.25',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        },
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.26',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        },
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.27',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        },
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.28',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        },
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.37',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        },
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.38',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        },
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.39',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        },
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.40',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        },
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.41',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        },
        {
            'device_type': 'alcatel_sros',
            'host': '10.42.10.42',
            'username': 'AliDoski',
            'password': 'Al!$osk!22',
        }
    ]

    all_data = [["Router Name", "Interface Name", "OSPF cfg Metric"]]

    for router_details in routers:
        data = get_router_info(router_details)
        if data:
            all_data.extend(data)

    pdf_file = "ospf_int_costs.pdf"
    generate_pdf(all_data, pdf_file)

if __name__ == "__main__":
    main()
