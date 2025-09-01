import socket
import threading
import time

BROADCAST_PORT = 50000
BROADCAST_INTERVAL = 3
BROADCAST_MESSAGE=b'DISCOVERY'

def create_socket():
    brodcaster=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #DGRAM refers to udp
    brodcaster.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #Letting the socket make brodcasts
    brodcaster.settimeout(2) #wait for 2 seconds and if nothig happens then ->timeout
    return brodcaster



