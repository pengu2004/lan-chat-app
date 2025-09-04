class ChatSession:
    """Peer socket is used to strore """
    def __init__(self): 
        self.messages=[]
        self.current_peer=None
        self.peer_socket=None
        self.my_name = None  
        self.peerlist={}

    def add_message(self,message):
        self.messages.append(message)
        