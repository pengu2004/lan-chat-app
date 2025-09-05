from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import time
import queue
import threading
from configs import Config

console = Console()

# Global variables for the display module (shared with NetworkManager)
messages = []
current_peer = None
peer_socket = None


class DisplayManager:
    """Handles UI display and user input for the chat application"""
    
    def __init__(self, network_manager):
        self.network_manager = network_manager
        self.input_queue = queue.Queue()
        
        # Start input thread
        self._start_input_thread()
    
    def _start_input_thread(self):
        """Start the non-blocking input thread"""
        input_thread = threading.Thread(target=self._get_input, daemon=True)
        input_thread.start()
    
    def _get_input(self):
        """Handle non-blocking user input"""
        while True:
            time.sleep(1)
            inp = input("<<<")
            self.input_queue.put(inp)
    
    def generate_table(self, peerlist):
        """Generate a table displaying the current peer list"""
        table = Table(title="Peerlist", border_style="green")
        table.add_column("IP address")
        table.add_column("Nickname")
        table.add_column("Ping")
        
        for (ip, port), info in peerlist.items():
            table.add_row(
                f"[red]{ip}:{port}[red]",
                info["name"],
                str(round(time.time() - info["time_stamp"], 2))
            )
        return table
    
    def display_name(self, my_name):
        """Display the current user's name"""
        status_text = Text(f"• {my_name}", style="bold green")
        name_panel = Panel(status_text, title="You", border_style="green")
        return name_panel
    
    def chat_box(self, peerlist):
        """Handle chat box display and message processing"""
        global current_peer, messages, peer_socket
        
        if not self.input_queue.empty():
            inp = self.input_queue.get()
            
            # Select a peer
            if current_peer is None:
                peer_found = False
                for (ip, port), info in peerlist.items():
                    if inp == info["name"]:
                        current_peer = info["name"]
                        ip_address = ip
                        
                        # Create client connection using NetworkManager
                        peer_socket = self.network_manager.create_client_connection(
                            ip_address, Config.SERVER_PORT
                        )
                        
                        return Panel(f"Successfully connected{peer_socket}", title="Connected")
                
                if not peer_found:
                    return Panel(
                        Text(f"{inp} is not online or nickname is incorrect.", style="red"),
                        title="Error"
                    )
            
            # Send a message
            else:
                messages.append(f"[bold red] You:[/bold red] {inp}")
                try:
                    peer_socket.send(inp.encode())
                except Exception as e:
                    messages.append(f"[red]Failed to send: {e}[/red]")
        
        # Display chat history
        if current_peer:
            chat_history = Text.from_markup("\n".join(messages))
            return Panel(
                chat_history,
                title=f"Chatting with {current_peer}",
                border_style="blue"
            )
        else:
            return Panel(
                Text("Enter the nickname of the person you want to chat with"),
                title="Chat"
            )