import socket
import threading
import time
from rich.console import Console
console=Console()

BROADCAST_PORT = 50000
BROADCAST_INTERVAL = 3
BROADCAST_MESSAGE=b'DISCOVERY'
WAIT_TIME=10
peerlist={}
peer_lock = threading.Lock()

def create_socket():
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #DGRAM refers to udp
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #Letting the socket make brodcasts
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
    sock.settimeout(2) #wait for 2 seconds and if nothig happens then ->timeout
    return sock

def im_alive(peerlist,my_name): #use to broadcast that  I am alive
    broadcaster=create_socket()
    while True:
        nick_name=my_name.encode("utf-8")
        broadcaster.sendto(BROADCAST_MESSAGE+nick_name,('255.255.255.255',BROADCAST_PORT))
        print(peerlist)
        print("Broadcaster is online")
        time.sleep(BROADCAST_INTERVAL)
        
def are_you_there(peerlist,peer_lock): 
    listner=create_socket()
    listner.bind(("",BROADCAST_PORT))#listening to the broadcast port 
    while True:

        try:
            with peer_lock:
                data,addr=listner.recvfrom(1024)
                if data.startswith(BROADCAST_MESSAGE) and addr not in peerlist and name not in data.decode():
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
            to_remove=[]
            for address,info in peerlist.items():
                last_seen=info["time_stamp"]
                if current_time-last_seen>=WAIT_TIME: 
                    to_remove.append(address)
                    print("Removed",info["name"]) #removal message
            for addr in to_remove:
                peerlist.pop(addr)







if __name__== "__main__":
    console.print("Hii Welcome",style="bold red")
    name=input("Enter your name")
    im_alive_thread = threading.Thread(target=im_alive,args=(peerlist,name))
    are_you_there_thread = threading.Thread(target=are_you_there, args=(peerlist,peer_lock))
    cleaner_thread=threading.Thread(target=cleaner,args=(peerlist,peer_lock))

    im_alive_thread.start()
    are_you_there_thread.start()
    cleaner_thread.start()
    
#todo use rich.Live to make a peer table









