import socket
import threading
import time

BROADCAST_PORT = 50000
BROADCAST_INTERVAL = 3
BROADCAST_MESSAGE=b'DISCOVERY'
peerlist=[]
def create_socket():
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #DGRAM refers to udp
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #Letting the socket make brodcasts
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
    sock.settimeout(2) #wait for 2 seconds and if nothig happens then ->timeout
    return sock

def im_alive(): #use to broadcast that  I am alive
    broadcaster=create_socket()
    while True:
        broadcaster.sendto(BROADCAST_MESSAGE,('255.255.255.255',BROADCAST_PORT))
        print("Broadcaster is online")
        time.sleep(BROADCAST_INTERVAL)
        
def are_you_there(peerlist): 
    listner=create_socket()
    listner.bind(("",BROADCAST_PORT))
    while True:
        try:
            data,addr=listner.recvfrom(1024)
            if data==BROADCAST_MESSAGE and addr not in peerlist:
                print("Peer found",addr)
                peerlist.append(addr)
            if addr in peerlist:
                print(data)
           
        except socket.timeout:
            print(peerlist[1:])
            print("Listening..")

if __name__== "__main__":
    name=input("Enter your name")
    im_alive_thread = threading.Thread(target=im_alive)
    are_you_there_thread = threading.Thread(target=are_you_there, args=(peerlist,))
    im_alive_thread.start()
    are_you_there_thread.start()
    
            








