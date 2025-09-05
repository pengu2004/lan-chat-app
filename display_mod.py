from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
import time
import queue
import threading
from network import create_discovery_socket, create_client
from configs import Config

console = Console()


class DisplayManager:
    """Handles UI display and user input for the chat application"""
    
    def __init__(self, network_manager):
        self.network_manager = network_manager
        self.messages = []
        self.current_peer = None
        self.peer_socket = None
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
        if not self.input_queue.empty():
            inp = self.input_queue.get()
            
            # Select a peer
            if self.current_peer is None:
                peer_found = False
                for (ip, port), info in peerlist.items():
                    if inp == info["name"]:
                        self.current_peer = info["name"]
                        ip_address = ip
                        port_number = port
                        
                        # Create client connection using NetworkManager
                        self.peer_socket = self.network_manager.create_client_connection(
                            ip_address, Config.SERVER_PORT
                        )
                        
                        return Panel(f"Successfully connected{self.peer_socket}", title="Connected")
                
                if not peer_found:
                    return Panel(
                        Text(f"{inp} is not online or nickname is incorrect.", style="red"),
                        title="Error"
                    )
            
            # Send a message
            else:
                self.messages.append(f"[bold red] You:[/bold red] {inp}")
                try:
                    self.peer_socket.send(inp.encode())
                except Exception as e:
                    self.messages.append(f"[red]Failed to send: {e}[/red]")
        
        # Display chat history
        if self.current_peer:
            chat_history = Text.from_markup("\n".join(self.messages))
            return Panel(
                chat_history,
                title=f"Chatting with {self.current_peer}",
                border_style="blue"
            )
        else:
            return Panel(
                Text("Enter the nickname of the person you want to chat with"),
                title="Chat"
            )


# Global variables for backward compatibility (will be removed after full refactoring)
input_queue = queue.Queue()
messages = []
current_peer = None
peer_socket = None


def get_input():
    """Legacy function - use DisplayManager class instead"""
    while True:
        time.sleep(1)
        inp = input("<<<")
        input_queue.put(inp)


# Start legacy input thread for backward compatibility
threading.Thread(target=get_input, daemon=True).start()


# Legacy functions for backward compatibility
def generate_table(peerlist):
    """Legacy function - use DisplayManager class instead"""
    display = DisplayManager(None)
    return display.generate_table(peerlist)


def display_name(my_name):
    """Legacy function - use DisplayManager class instead"""
    display = DisplayManager(None)
    return display.display_name(my_name)


def chat_box(peerlist):
    """Legacy function - use DisplayManager class instead"""
    from network import NetworkManager
    network_manager = NetworkManager(peerlist)
    display = DisplayManager(network_manager)
    display.input_queue = input_queue
    display.messages = messages
    display.current_peer = current_peer
    display.peer_socket = peer_socket
    return display.chat_box(peerlist)