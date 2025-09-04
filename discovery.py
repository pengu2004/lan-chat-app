import socket
import time
import threading
from rich.console import Console
from configs import BROADCAST_INTERVAL, BROADCAST_MESSAGE, BROADCAST_PORT, WAIT_TIME
from network import create_discovery_socket

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
        while not self.stop_event.set():
            try:
                broadcaster.sendto(BROADCAST_MESSAGE+nick_name,('255.255.255.255',BROADCAST_PORT))
                self.console.print(f"[green]Broadcaster is online[/green]{self.my_name}")
            except Exception as e:
                self.console.print(f"[red]Broadcast error: {e}[/red]")

            time.sleep(BROADCAST_INTERVAL) #broadcast only in intervals

    def _listen_for_peers(self):
        listener=create_discovery_socket()
        listener.bind(("",BROADCAST_PORT))#listening to the broadcast port 
        listener.settimeout(2)
        while not self.stop_event.set():
            try:
                data,addr=listener.recv(1024)
                received_from_self=self.my_name not in data.decode() #to check if revcived from self
                discovery_message=data.startswith(BROADCAST_MESSAGE)
                is_new_peer=addr not in self.peerlist
                if data.startswith(BROADCAST_MESSAGE) and not received_from_self:
                    nickname = data[len(BROADCAST_MESSAGE):].decode('utf-8')
                    if is_new_peer:
                        with self.peer_lock:
                            self.peerlist[addr]={"name":nickname,"timestamp":time.time()} #creating a new entry in the peerlist
                            self.console.print(f"[blue]Peer found: {nickname} at {addr}[/blue]")
                    else:
                        with self.peer_lock:
                            self.peerlist[addr]["time_stamp"] = time.time()
                            self.console.print(f"[blue]Peer Updated:[/blue]")



        
# def are_you_there(peerlist,peer_lock,my_name): 
#     listner=create_discovery_socket()
#     listner.bind(("",BROADCAST_PORT))#listening to the broadcast port 
#     while True:

#         try:
#             with peer_lock:
#                 data,addr=listner.recvfrom(1024)
#                 print(data)
#                 if data.startswith(BROADCAST_MESSAGE) and addr not in peerlist and my_name not in data.decode():
#                     print("Peer found",addr)
#                     data=data.split(BROADCAST_MESSAGE)
#                     peerlist[addr]={"name":data[1].decode('utf-8'),"time_stamp":time.time()} #decoding the message to add the nickname
#                     print(peerlist)
#                 elif addr in peerlist:
#                     peerlist[addr]["time_stamp"]=time.time()# updating the time
#         except socket.timeout:
#             print("Listening..")

# def cleaner(peerlist,peer_lock):
#     while True:
#         with peer_lock:
#             current_time=time.time()
#             to_remove=[] #adding the items to remove
#             for address,info in peerlist.items():
#                 last_seen=info["time_stamp"]
#                 if current_time-last_seen>=WAIT_TIME: 
#                     to_remove.append(address)
#                     print("Removed",info["name"]) #removal message
#             for addr in to_remove:
#                 peerlist.pop(addr)
