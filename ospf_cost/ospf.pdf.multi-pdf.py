import re
from netmiko import ConnectHandler
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import time

# Function to read router details from igws.txt file
def read_router_details(file_path):
    routers = []
    with open(file_path, 'r') as file:
        for line in file:
            ip, system_name = line.strip().split()
            routers.append({'ip': ip, 'system_name': system_name})
    return routers

# Function to connect to each router and retrieve OSPF interface details
def retrieve_ospf_details(router_details):
    try:
        # Connect to the router
        ssh_session = ConnectHandler(device_type='alcatel_sros', host=router_details['ip'],
                                      username='AliDoski', password='Al!$osk!22')
        
        # Send command to get OSPF interface details
        ospf_output = ssh_session.send_command("show router ospf interface detail")

        # Extract interface name and cfg Metric using regular expressions
        interfaces = re.split(r'(?=Interface : )', ospf_output)  # Split by Interface

        data = []
        for interface in interfaces:
            match = re.search(r'Interface : (.+)', interface)
            if match:
                interface_name = match.group(1).strip()
                cfg_metric_match = re.search(r'Cfg Metric\s*:\s*(\d+)', interface)
                if cfg_metric_match:
                    cfg_metric = cfg_metric_match.group(1).strip()
                    data.append([router_details['system_name'], interface_name, cfg_metric])

        # Close the SSH session
        ssh_session.disconnect()

        return data

    except Exception as e:
        print(f"An error occurred while retrieving OSPF details for {router_details['system_name']}: {str(e)}")
        return []

# Main function to generate PDF
def generate_pdf(data, pdf_file):
    try:
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
        print("An error occurred while generating PDF:", str(e))

if __name__ == "__main__":
    try:
        # Read router details from igws.txt file
        routers = read_router_details('igws.txt')

        all_data = [["Router Name", "Interface Name", "OSPF cfg Metric"]]

        for router in routers:
            print(f"Retrieving OSPF details for router {router['system_name']}...")
            data = retrieve_ospf_details(router)
            all_data.extend(data)
            time.sleep(5)  # Introduce a delay of 5 seconds

        # Generate PDF
        generate_pdf(all_data, "ospf_interface_details.pdf")

    except Exception as e:
        print("An error occurred:", str(e))
