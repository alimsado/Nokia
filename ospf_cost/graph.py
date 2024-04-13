import re
from netmiko import ConnectHandler
import networkx as nx
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Router details
router = {
    'device_type': 'alcatel_sros',
    'host': '10.42.10.37',
    'username': 'AliDoski',
    'password': 'Al!$osk!22',
    'verbose': True  # Set verbose to True to increase debugging output
}

# Function to retrieve OSPF interface details
def retrieve_ospf_details(router_details):
    try:
        # Connect to the router
        ssh_session = ConnectHandler(**router_details)
        
        # Send command to get OSPF interface details
        output = ssh_session.send_command("show router interface")
        
        # Extract interface names
        interfaces = re.findall(r'Interface\s+:\s+(\S+)', output)
        
        # Close the SSH session
        ssh_session.disconnect()

        return interfaces

    except Exception as e:
        print(f"An error occurred while retrieving OSPF details: {str(e)}")
        return []

# Function to generate circular graph
def generate_circular_graph(interfaces, pdf_file):
    try:
        # Create a graph
        G = nx.cycle_graph(len(interfaces))

        plt.figure(figsize=(8, 8))
        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold')
        plt.axis('off')
        plt.savefig("router_interfaces_graph.png", format="PNG")
        
        # Generate PDF with graph image
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawString(100, 750, "Router Interfaces Circular Graph")
        
        # Add image to PDF
        c.drawImage("router_interfaces_graph.png", 100, 100, width=400, height=400)
        
        c.showPage()
        c.save()

        print(f"PDF with circular graph generated successfully: {pdf_file}")

    except Exception as e:
        print("An error occurred while generating PDF with circular graph:", str(e))

if __name__ == "__main__":
    try:
        # Retrieve OSPF interface details
        print("Retrieving OSPF interface details...")
        interfaces = retrieve_ospf_details(router)
        
        # Generate circular graph and PDF
        generate_circular_graph(interfaces, "router_interfaces_graph.pdf")

    except Exception as e:
        print("An error occurred:", str(e))
