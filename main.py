import socket
import threading
import time
from rich.console import Console
from rich.live import Live
from rich.layout import Layout

from configs import Config
from discovery import PeerDiscovery
from network import NetworkManager
from display_mod import DisplayManager

# Legacy imports for backward compatibility
from display_mod import generate_table, display_name, chat_box
from discovery import im_alive, are_you_there, cleaner
from network import create_server

console = Console()


class ChatApplication:
    """Main chat application controller"""
    
    def __init__(self):
        self.console = Console()
        self.name = None
        self.peer_discovery = None
        self.network_manager = None
        self.display_manager = None
        
    def setup(self):
        """Set up the application components"""
        self.console.print("Hii Welcome", style="bold red")
        self.name = self.console.input("What is [i]your[/i] [bold red]name[/]?  ")
        
        # Initialize components
        self.peer_discovery = PeerDiscovery(self.name)
        self.network_manager = NetworkManager(self.peer_discovery.peerlist)
        self.display_manager = DisplayManager(self.network_manager)
        
    def start_services(self):
        """Start all background services"""
        # Start peer discovery
        discovery_threads = self.peer_discovery.start_discovery()
        
        # Start network server
        server_thread = self.network_manager.start_server()
        
        return discovery_threads + (server_thread,)
    
    def run_ui(self):
        """Run the main UI loop"""
        # Set up the layout
        layout = Layout(name="root")
        layout.split_row(
            Layout(name="left"),
            Layout(name="right", ratio=3)
        )
        layout["right"].split_column(
            Layout(name="right_header", size=3),  # A small top section for name
            Layout(name="right_body")
        )
        
        time.sleep(1)  # Give the server a moment to start
        
        with Live(layout, refresh_per_second=Config.REFRESH_RATE) as live:
            while True:
                peerlist = self.peer_discovery.get_peerlist()
                
                layout["left"].update(self.display_manager.generate_table(peerlist))
                layout["right_header"].update(self.display_manager.display_name(self.name))
                layout["right_body"].update(self.display_manager.chat_box(peerlist))
                
                live.update(layout)
                time.sleep(Config.UI_UPDATE_INTERVAL)
    
    def run(self):
        """Run the complete application"""
        self.setup()
        self.start_services()
        self.run_ui()


def main():
    """Main entry point using new class structure"""
    app = ChatApplication()
    app.run()


# Legacy main code for backward compatibility
def legacy_main():
    """Original main code - kept for backward compatibility"""
    peerlist = {}
    peer_lock = threading.Lock()

    console.print("Hii Welcome", style="bold red")
    name = console.input("What is [i]your[/i] [bold red]name[/]?  ")

    im_alive_thread = threading.Thread(target=im_alive, args=(peerlist, name))
    are_you_there_thread = threading.Thread(target=are_you_there, args=(peerlist, peer_lock, name))
    cleaner_thread = threading.Thread(target=cleaner, args=(peerlist, peer_lock))
    server = threading.Thread(target=create_server, args=(peerlist,))
    
    im_alive_thread.start()
    are_you_there_thread.start()
    cleaner_thread.start()
    server.start()

    # Main part of display
    # Dividing the screen into 2 parts
    layout = Layout(name="root")
    layout.split_row(
        Layout(name="left"),
        Layout(name="right", ratio=3)
    )
    layout["right"].split_column(
        Layout(name="right_header", size=3),  # A small top section for name
        Layout(name="right_body")
    )
    time.sleep(1)  # Give the server a moment to start

    with Live(layout, refresh_per_second=4) as live:
        while True:
            layout["left"].update(generate_table(peerlist))
            layout["right_header"].update(display_name(name))
            layout["right_body"].update(chat_box(peerlist))

            live.update(layout)
            time.sleep(0.4)


if __name__ == "__main__":
    # Use the new class-based approach
    main()
    
    # To use legacy approach, uncomment the following line instead:
    # legacy_main()











