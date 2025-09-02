from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import time
console=Console()

def generate_table(peerlist):
    table = Table(title="Peerlist")
    table.add_column("IP address")
    table.add_column("Nickname")
    table.add_column("Ping")
    for (ip,port),info in peerlist.items():
        table.add_row(info["name"], f"{ip}:{port}", str(round(time.time() - info["time_stamp"], 3)))
        
    return table
def display_name(my_name):
    status_text =Text(f"• {my_name}", style="bold green")
    
    name_panel =Panel(status_text, title="You", border_style="green")
    return name_panel

