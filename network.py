import socket
import threading
import time

BROADCAST_PORT = 6000
DISCOVERY_MSG = b"DISCOVERY_REQUEST"
peer=[]

def send_broadcast():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        udp_socket.sendto(DISCOVERY_MSG, ('<broadcast>', BROADCAST_PORT))
        print("Broadcast sent")
        time.sleep(5)  # send every 5 seconds

def listen_for_peers():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", BROADCAST_PORT))

    while True:
        data, addr = udp_socket.recvfrom(1024)
        if data == DISCOVERY_MSG:
            print(f"Discovery request from {addr}")
            # send back a response
            udp_socket.sendto(b"DISCOVERY_RESPONSE", addr)
        elif data == b"DISCOVERY_RESPONSE":
            peer.append(addr)
            print(f"Peer found: {addr}")
            print(peer)

if __name__ == "__main__":
    threading.Thread(target=send_broadcast, daemon=True).start()
    listen_for_peers()