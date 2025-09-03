from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
import time
import queue
import threading
from network import create_discovery_socket,create_client
input_queue=queue.Queue()

messages = []       # store chat history
current_peer = None # store selected peer name
peer_socket = None
console=Console()

def generate_table(peerlist):
    table = Table(title="Peerlist",border_style="green")
    table.add_column("IP address")
    table.add_column("Nickname")
    table.add_column("Ping")
    for (ip, port), info in peerlist.items():
        table.add_row(f"[red]{ip}:{port}[red]", info["name"], str(round(time.time() - info["time_stamp"], 2)))
    return table
def display_name(my_name):
    status_text =Text(f"• {my_name}", style="bold green")
    
    name_panel =Panel(status_text, title="You", border_style="green")
    return name_panel

def get_input():
    while True:
        time.sleep(1)
        inp=input("<<<")
        input_queue.put(inp)

threading.Thread(target=get_input, daemon=True).start()# allow non blocking user input
def chat_box(peerlist):
    global current_peer
    global messages

   
    if not input_queue.empty():
        inp = input_queue.get()
        
       
        if current_peer is None:
            peer_found = False
            for (ip, port), info in peerlist.items():
                if inp == info["name"]:

                    current_peer = inp
                    peer_found = True
                    s=create_client(ip,port)
                    peer_socket[current_peer]=s
                    return Panel("Successfully connected", title="Connected")
                    break
            
            if not peer_found:
                error_text = Text(f"{inp} is not online or nickname is incorrect.", style="red")
                return Panel(error_text, title="Error")

        else:
            messages.append(f"[bold red]You:[/bold red] {inp}")
            
    if current_peer:
        chat_history = Text("\n".join(messages))
        chat_history_panel = Panel(chat_history, title=f"Chatting with {current_peer}", border_style="blue")
        #send and receive messages

        
        
        return chat_history_panel
    else:
        prompt_text = Text("Enter the nickname of the person you want to chat with")
        return Panel(prompt_text, title="Chat")

