from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
import time
import queue
import threading
from network import create_discovery_socket, create_client

input_queue = queue.Queue()
messages = []        # store chat history
current_peer = None  # store selected peer name
peer_socket = {}     # FIXED: use a dict
console = Console()

def generate_table(peerlist):
    table = Table(title="Peerlist", border_style="green")
    table.add_column("IP address")
    table.add_column("Nickname")
    table.add_column("Ping")
    for (ip, port), info in peerlist.items():
        table.add_row(f"[red]{ip}:{port}[red]", info["name"], str(round(time.time() - info["time_stamp"], 2)))
    return table

def display_name(my_name):
    status_text = Text(f"• {my_name}", style="bold green")
    return Panel(status_text, title="You", border_style="green")

def get_input():
    while True:
        inp = input("<<< ")
        input_queue.put(inp)

threading.Thread(target=get_input, daemon=True).start()  # allow non-blocking user input

def connect_to_peer(ip, port, peer_name):
    """Run client connection in a separate thread to avoid blocking"""
    s = create_client(ip, port)
    if s:
        peer_socket[peer_name] = s
        console.print(f"[green]Successfully connected to {peer_name}[/green]")
    else:
        console.print(f"[red]Failed to connect to {peer_name}[/red]")

def chat_box(peerlist):
    global current_peer, messages, peer_socket

    if not input_queue.empty():
        inp = input_queue.get()

        # Select a peer
        if current_peer is None:
            peer_found = False
            for (ip, port), info in peerlist.items():
                if inp == info["name"]:
                    # Start client connection in a thread to avoid blocking
                    threading.Thread(target=connect_to_peer, args=(ip, port, inp), daemon=True).start()
                    peer_found = True
                    return Panel("Connecting...", title="Info")
            if not peer_found:
                return Panel(Text(f"{inp} is not online or nickname is incorrect.", style="red"), title="Error")

        # Send a message
        else:
            messages.append(f"[bold red]You:[/bold red] {inp}")
            try:
                peer_socket[current_peer].send(inp.encode())
            except Exception as e:
                messages.append(f"[red]Failed to send: {e}[/red]")

    # Display chat history
    if current_peer:
        chat_history = Text("\n".join(messages))
        return Panel(chat_history, title=f"Chatting with {current_peer}", border_style="blue")
    else:
        return Panel(Text("Enter the nickname of the person you want to chat with"), title="Chat")