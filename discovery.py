import socket
import time
from rich.console import Console
from configs import BROADCAST_INTERVAL,BROADCAST_MESSAGE,BROADCAST_PORT,WAIT_TIME
from network import create_socket
console=Console()



def im_alive(peerlist,my_name): #use to broadcast that  I am alive
    broadcaster=create_socket()
    while True:
        nick_name=my_name.encode("utf-8")
        broadcaster.sendto(BROADCAST_MESSAGE+nick_name,('255.255.255.255',BROADCAST_PORT))
        print(peerlist)
        print("Broadcaster is online")
        time.sleep(BROADCAST_INTERVAL)
        
def are_you_there(peerlist,peer_lock,my_name): 
    listner=create_socket()
    listner.bind(("",BROADCAST_PORT))#listening to the broadcast port 
    while True:

        try:
            with peer_lock:
                data,addr=listner.recvfrom(1024)
                if data.startswith(BROADCAST_MESSAGE) and addr not in peerlist and my_name not in data.decode():
                    print("Peer found",addr)
                    data=data.split(BROADCAST_MESSAGE)
                    peerlist[addr]={"name":data[1].decode('utf-8'),"time_stamp":time.time()} #decoding the message to add the nickname
                    print(peerlist)
                elif addr in peerlist:
                    peerlist[addr]["time_stamp"]=time.time()# updating the time
        except socket.timeout:
            print("Listening..")

def cleaner(peerlist,peer_lock):
    while True:
        with peer_lock:
            current_time=time.time()
            to_remove=[] #adding the items to remove
            for address,info in peerlist.items():
                last_seen=info["time_stamp"]
                if current_time-last_seen>=WAIT_TIME: 
                    to_remove.append(address)
                    print("Removed",info["name"]) #removal message
            for addr in to_remove:
                peerlist.pop(addr)
