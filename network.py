import socket
import threading
import time

BROADCAST_PORT = 50000
BROADCAST_INTERVAL = 3
BROADCAST_MESSAGE=b'DISCOVERY'

def create_socket():
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #DGRAM refers to udp
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #Letting the socket make brodcasts
    sock.settimeout(2) #wait for 2 seconds and if nothig happens then ->timeout
    return sock

def are_you_there(peerlist): #use to add new peers or check if the existing ones are there
    broadcaster=create_socket()
    while True:
        broadcaster.sendto(BROADCAST_MESSAGE,('255,255,255,255',BROADCAST_PORT))
        print("Broadcaster is online")
        time.sleep(BROADCAST_INTERVAL)




