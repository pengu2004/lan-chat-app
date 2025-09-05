import socket
import time
import threading
from rich.console import Console
from configs import Config
from network import NetworkManager

console = Console()


class PeerDiscovery:
    """Handles peer discovery and management in the network"""
    
    def __init__(self, my_name):
        self.my_name = my_name
        self.peerlist = {}
        self.peer_lock = threading.Lock()
        self.broadcaster = None
        self.listener = None
        self.network_manager = NetworkManager(self.peerlist)
        
    def get_peerlist(self):
        """Get a copy of the current peer list"""
        with self.peer_lock:
            return self.peerlist.copy()
    
    def start_discovery(self):
        """Start the peer discovery process"""
        # Start broadcaster thread
        broadcaster_thread = threading.Thread(target=self._broadcast_presence, daemon=True)
        broadcaster_thread.start()
        
        # Start listener thread  
        listener_thread = threading.Thread(target=self._listen_for_peers, daemon=True)
        listener_thread.start()
        
        # Start cleaner thread
        cleaner_thread = threading.Thread(target=self._clean_inactive_peers, daemon=True)
        cleaner_thread.start()
        
        return broadcaster_thread, listener_thread, cleaner_thread
    
    def _broadcast_presence(self):
        """Broadcast that this peer is alive"""
        self.broadcaster = self.network_manager.create_discovery_socket()
        while True:
            nick_name = self.my_name.encode("utf-8")
            self.broadcaster.sendto(
                Config.BROADCAST_MESSAGE + nick_name,
                ('255.255.255.255', Config.BROADCAST_PORT)
            )
            print(self.peerlist)
            print("Broadcaster is online")
            time.sleep(Config.BROADCAST_INTERVAL)
    
    def _listen_for_peers(self):
        """Listen for other peers broadcasting their presence"""
        self.listener = self.network_manager.create_discovery_socket()
        self.listener.bind(("", Config.BROADCAST_PORT))
        
        while True:
            try:
                with self.peer_lock:
                    data, addr = self.listener.recvfrom(1024)
                    print(data)
                    if (data.startswith(Config.BROADCAST_MESSAGE) and 
                        addr not in self.peerlist and 
                        self.my_name not in data.decode()):
                        
                        print("Peer found", addr)
                        data = data.split(Config.BROADCAST_MESSAGE)
                        self.peerlist[addr] = {
                            "name": data[1].decode('utf-8'),
                            "time_stamp": time.time()
                        }
                        print(self.peerlist)
                    elif addr in self.peerlist:
                        # Update timestamp for existing peer
                        self.peerlist[addr]["time_stamp"] = time.time()
            except socket.timeout:
                print("Listening..")
    
    def _clean_inactive_peers(self):
        """Remove peers that haven't been seen recently"""
        while True:
            with self.peer_lock:
                current_time = time.time()
                to_remove = []
                
                for address, info in self.peerlist.items():
                    last_seen = info["time_stamp"]
                    if current_time - last_seen >= Config.WAIT_TIME:
                        to_remove.append(address)
                        print("Removed", info["name"])
                
                for addr in to_remove:
                    self.peerlist.pop(addr)
