import socket
import threading

def create_discovery_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.settimeout(2)
    return sock

def receive_tcp_message(sock, callback=None):
    """Receive TCP messages in a thread"""
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            if callback:
                callback(data)
        except Exception as e:
            if callback:
                callback(f"[Error receiving message: {e}]")
            break

def create_server(port=7777):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", port))
    server.listen(5)
    print(f"Server listening on port {port}...")
    while True:
        conn, addr = server.accept()
        print("Server: You are connected to", addr)
        threading.Thread(target=receive_tcp_message, args=(conn,), daemon=True).start()

def create_client(ip, port=7777):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)  # timeout for connect
        s.connect((ip, port))
        s.settimeout(None)  # remove timeout after connecting
        threading.Thread(target=receive_tcp_message, args=(s,), daemon=True).start()
        return s
    except Exception as e:
        print("Client connection error:", e)
        return None