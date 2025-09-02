from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
import time
import queue
import threading
input_queue=queue.Queue()
messages = []       # store chat history
current_peer = None # store selected peer name

console=Console()

def generate_table(peerlist):
    table = Table(title="Peerlist")
    table.add_column("IP address")
    table.add_column("Nickname")
    table.add_column("Ping")
    for (ip, port), info in peerlist.items():
        table.add_row(f"{ip}:{port}", info["name"], str(round(time.time() - info["time_stamp"], 2)))
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
    global current_peer #can chat to only 1 peer for now
    if current_peer:
            return Panel(f"You are chatting with {current_peer}", title=current_peer, border_style="blue")

    while not input_queue.empty():
        inp=input_queue.get()
        if current_peer is None:
            for (ip, port), info in peerlist.items():
                if inp==info["name"]:
                    current_peer=inp
                    return Panel(f"You are now chatting with {current_peer}", title=current_peer, border_style="blue")
            error_text = Text(f"{inp} is not online or nickname is incorrect.", style="red")
            return Panel(error_text)
    prompt_text = Text("Enter the nickname of the person you want to chat with")
    return Panel(prompt_text, title="Chat")


    


    
