import socket
import threading
import time

def create_discovery_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #dgram for udp
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.settimeout(2)
    return sock


def receive_message(sock):
    import display_mod
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            display_mod.messages.append(f"[bold cyan]{display_mod.current_peer}:[/bold cyan] {data}")
        except Exception as e:
            display_mod.messages.append(f"[red]Error receiving message: {e}[/red]")
            break
#creating a server to accept connecitons
def create_server():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    server.bind(("", 7777))
    server.listen(5)
    while True:
        conn,port=server.accept()
        print("Server:You are connected to",conn,"at port",port)
        threading.Thread(target=receive_message, args=(conn,), daemon=True).start()
        

def create_client(ip,port=7777):# this happens when a user has chosen a correct name in the peer list
    try:
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((ip, port))
        peer_socket.settimeout(2)
        threading.Thread(target=receive_message, args=(peer_socket,), daemon=True).start()
        return peer_socket
    except Exception as e:
        print("There was an error",e)


