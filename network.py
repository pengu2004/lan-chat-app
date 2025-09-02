import socket

def create_socket():
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #DGRAM refers to udp
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #Letting the socket make brodcasts
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
    sock.settimeout(2) #wait for 2 seconds and if nothig happens then ->timeout
    return sock
