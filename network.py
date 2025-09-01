import socket
import threading
import time

BROADCAST_PORT = 50000
BROADCAST_INTERVAL = 3
BROADCAST_MESSAGE=b'DISCOVERY'
WAIT_TIME=10
peerlist={}
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
        
def are_you_there(peerlist): 
    listner=create_socket()
    listner.bind(("",BROADCAST_PORT))
    while True:
        try:
            data,addr=listner.recvfrom(1024)
            if data.startswith(BROADCAST_MESSAGE) and addr not in peerlist:
                print("Peer found",addr)
                data=data.split(BROADCAST_MESSAGE)
                peerlist[addr]=[data[1].decode('utf-8'),time.time()] #decoding the message to add the nickname
                print(peerlist)
            elif addr in peerlist:
                peerlist[addr][1]=time.time()# updating the time
        except socket.timeout:
            print("Listening..")
            cleaner(peerlist)

def cleaner(peerlist):
    current_time=time.time()
    to_remove=[]
    for address,info in peerlist.items():
        last_seen=info[1]
        if current_time-last_seen>=WAIT_TIME:
            to_remove.append(address)
            print("Removed",info[0]) #removal message
    for addr in to_remove:
        
        peerlist.pop(addr)






if __name__== "__main__":
    name=input("Enter your name")
    im_alive_thread = threading.Thread(target=im_alive,args=(peerlist,name))
    are_you_there_thread = threading.Thread(target=are_you_there, args=(peerlist,))
    im_alive_thread.start()
    are_you_there_thread.start()
    
            








