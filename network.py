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




#creating a server to accept connecitons
def create_server():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    server.bind(("", 7777))
    server.listen(5)
    print("Server has started")
    while True:
        conn,port=server.accept()
        print("Server:You are connected to",conn,"at port",port)
        message=conn.recv(1024)
        print(message)    
        thread = threading.Thread(target=recieve_message, args=(conn,), daemon=True)
        thread.start()



        
        
def create_client(ip,port):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send(b"heyy")
    thread = threading.Thread(target=recieve_message, args=(client,), daemon=True)
    thread.start()
    


def recieve_message(sock,name):
    import display_mod
    while True:
        data = sock.recv(1024)
        if not data:   # connection closed
            break
        display_mod.messages.append(f"[bold red]{name}{data.decode()}")                                                                                                  
        print("Message received")
        print(display_mod.messages)

