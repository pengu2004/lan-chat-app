import socket
import threading
import time
import platform

def create_discovery_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # SO_REUSEPORT is not supported on Windows
    if platform.system() != "Windows":
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.settimeout(2)
    return sock

def create_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", 7777))
    server.listen(5)
    print("Server has started")
    while True:
        conn, addr = server.accept()
        print(f"Server: You are connected to {addr[0]} at port {addr[1]}")
        thread = threading.Thread(target=recieve_message, args=(conn, f"Client {addr[1]}"), daemon=True)
        thread.start()

        message = conn.recv(1024)
        print(message.decode())
       
def create_client(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(ip, port)

        
    client.connect((ip, port))
    print(f"Client connected to {ip}:{port}")

    thread = threading.Thread(target=recieve_message, args=(client, "Server"), daemon=True)
    thread.start()
    return client


def recieve_message(sock, name):
    import display_mod
    while True: 
        try:
            data = sock.recv(1024)
            if not data:
                print(f"Connection from {name} closed.")
                break
            # Append message to the list in the display module
            display_mod.messages.append(f"[bold blue]{name}: {data.decode()}")
            print(f"Message received from {name}")
            print(display_mod.messages)
        except (socket.error, ConnectionResetError) as e:
            print(f"Connection error with {name}: {e}")
            break
