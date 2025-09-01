import socket
import threading
name=str(input("Enter your name"))
peers=[]
def discovery():
        udp_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

        message=b'Any peers'
        udp_socket.sendto(message,('<brodcast>',6000))
        udp_socket.settimeout(2)
        while True:
                try:
                    data,addr=udp_socket.recvfrom(1024)
                    peers.append(addr)
                    print("A new peer was added")
                    print(data)
                except TimeoutError:
                       print("No peer found retrying...")
def listener():
    udp_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_socket.bind(('',6000))
    while True:
                data,addr=udp_socket.recvfrom(1024)
                if data==b'Any peers':
                    print("Discovery request from",addr)
                    udp_socket.sendto(b"Hello I am Peer", addr)
                       
if __name__ == "__main__":
    threading.Thread(target=listener, daemon=True).start()
    discovery()


