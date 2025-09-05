import socket
import threading
import platform
from configs import Config


class NetworkManager:
    """Handles network communications for the chat application"""
    
    def __init__(self, peerlist):
        self.peerlist = peerlist
        self.server_socket = None
        self.client_connections = {}
        
    def create_discovery_socket(self):
        """Create a socket for peer discovery"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # SO_REUSEPORT is not supported on Windows
        if platform.system() != "Windows":
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.settimeout(2)
        return sock
    
    def start_server(self):
        """Start the chat server"""
        server_thread = threading.Thread(target=self._run_server, daemon=True)
        server_thread.start()
        return server_thread
    
    def _run_server(self):
        """Run the chat server to accept incoming connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("", Config.SERVER_PORT))
        self.server_socket.listen(5)
        print("Server has started")
        
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Server: You are connected to {addr[0]} at port {addr[1]}")
            
            # Get peer name from peerlist
            peer_name = f" {self.peerlist[addr]['name']}" if addr in self.peerlist else "Unknown"
            
            thread = threading.Thread(
                target=self._handle_incoming_message, 
                args=(conn, peer_name), 
                daemon=True
            )
            thread.start()
            
            message = conn.recv(1024)
            print(message.decode())
    
    def create_client_connection(self, ip, port):
        """Create a client connection to another peer"""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(ip, port)
        
        client.connect((ip, Config.SERVER_PORT))
        print(f"Client connected to {ip}:{Config.SERVER_PORT}")
        
        thread = threading.Thread(
            target=self._handle_incoming_message, 
            args=(client, "Server"), 
            daemon=True
        )
        thread.start()
        return client
    
    def _handle_incoming_message(self, sock, name):
        """Handle incoming messages from a connection"""
        import display_mod
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    print(f"Connection from {name} closed.")
                    break
                display_mod.messages.append(f"[bold red]{name}: {data.decode()}")
                print(f"Message received from {name}")
                print(display_mod.messages)
            except (socket.error, ConnectionResetError) as e:
                print(f"Connection error with {name}: {e}")
                break


# Legacy functions for backward compatibility (will be removed after full refactoring)
def create_discovery_socket():
    """Legacy function - use NetworkManager class instead"""
    manager = NetworkManager({})
    return manager.create_discovery_socket()


def create_server(peerlist):
    """Legacy function - use NetworkManager class instead"""
    manager = NetworkManager(peerlist)
    manager._run_server()


def create_client(ip, port):
    """Legacy function - use NetworkManager class instead"""
    manager = NetworkManager({})
    return manager.create_client_connection(ip, port)


def recieve_message(sock, name):
    """Legacy function - use NetworkManager class instead"""
    manager = NetworkManager({})
    manager._handle_incoming_message(sock, name)
