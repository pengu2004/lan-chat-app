import socket
import time
import threading
from rich.console import Console
from configs import BROADCAST_INTERVAL, BROADCAST_MESSAGE, BROADCAST_PORT, WAIT_TIME
from network import create_discovery_socket
#todo impleement peer as a class to make it more structured
class PeerDiscovery:
    def __init__(self, my_name):
        self.my_name = my_name
        self.peerlist={}
        self.peer_lock=threading.Lock()
        self.console=Console()
        self.stop_event=threading.Event()

    def start(self):
        """Start all the threads"""
        threading.Thread(target=self._broadcast_alive, daemon=True).start()
        threading.Thread(target=self._listen_for_peers, daemon=True).start()
        threading.Thread(target=self._cleaner, daemon=True).start()

    def stop(self):
        """Make all the threads stop"""
        self.stop_event.set() #intiially set to False=>contains a boolean flag


    def _broadcast_alive(self): #use to broadcast that  I am alive (private method)
        broadcaster=create_discovery_socket()
        nick_name=self.my_name.encode("utf-8")
        while not self.stop_event.is_set():
            try:
                broadcaster.sendto(BROADCAST_MESSAGE+nick_name,('255.255.255.255',BROADCAST_PORT))
                self.console.print(f"[green]Broadcaster is online[/green] {self.my_name}")
            except Exception as e:
                self.console.print(f"[red]Broadcast error: {e}[/red]")

            time.sleep(BROADCAST_INTERVAL) #broadcast only in intervals

    def _listen_for_peers(self):
        listener=create_discovery_socket()
        listener.bind(("",BROADCAST_PORT))#listening to the broadcast port 
        listener.settimeout(2)
        while not self.stop_event.is_set():
            try:
                data,addr=listener.recvfrom(1024)
                print(data)
                received_from_self=self.my_name in data.decode() #to check if revcived from self
                discovery_message=data.startswith(BROADCAST_MESSAGE)
                is_new_peer=addr not in self.peerlist
                if discovery_message and not received_from_self:
                    nickname = data[len(BROADCAST_MESSAGE):].decode('utf-8')
                    if is_new_peer: #when we see a peer already in the peerlist
                        with self.peer_lock:
                            self.peerlist[addr]={"name":nickname,"timestamp":time.time()} #creating a new entry in the peerlist
                            self.console.print(f"[blue]Peer found: {nickname} at {addr}[/blue]")
                    else:
                        with self.peer_lock:
                            self.peerlist[addr]["timestamp"] = time.time()
                            self.console.print(f"[blue]Peer Updated:[/blue]")
            except socket.timeout:
                        self.console.print(f"[blue]Listening{nickname} at {addr}:[/blue]")
            except Exception as e:
                        self.console.print(f"[red]Error while listening:{e}[/red]")


    def _cleaner(self):
        while not self.stop_event.is_set():
            with self.peer_lock:
                current_time = time.time()
                to_remove = [addr for addr, info in self.peerlist.items()
                             if current_time - info["timestamp"] >= WAIT_TIME]

                for addr in to_remove:
                    self.console.print(f"[yellow]Removed peer: {self.peerlist[addr]['name']} at {addr}[/yellow]")
                    self.peerlist.pop(addr)

            time.sleep(WAIT_TIME)


        

