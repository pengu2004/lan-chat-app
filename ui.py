from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
import queue 
import threading,time
from network import create_client
class ChatUI:
    def __init__(self,session):
        self.console = Console()
        self.session=session
        self.input_queue=queue.Queue()
        threading.Thread(target=self._get_input, daemon=True).start()


    def _get_input(self):
        while True:
            time.sleep(0.1)
            inp = input("<<< ")
            self.input_queue.put(inp)



    def generate_table(self):
        """Show the peerlist as a table."""
        table = Table(title="Peerlist", border_style="green")
        table.add_column("IP address")
        table.add_column("Nickname")
        table.add_column("Ping")
        for (ip, port), info in self.session.peerlist.items():
            ping = str(round(time.time() - info["timestamp"], 2))
            table.add_row(f"[red]{ip}:{port}[/red]", info["name"], ping)
        return table
    


    def display_name(self):
        """Show current user's name."""
        status_text = Text(f"• {self.session.my_name}", style="bold green")
        return Panel(status_text, title="You", border_style="green")
    
    def chat_box(self):
         """Main chat area, handles input and displays messages"""
         if  not self.input_queue.empty(): #if something is being typed
            inp=self.input_queue.get() # typed     
            if self.session.current_peer is None: #that means inp was the first input and the user is selceting a peer
                self.session.peer_found=False
                for (ip,port),info in self.session.peerlist.items():
                    if inp==info["name"]:
                        self.session.current_peer=inp
                        self.session.peer_found=True
                        print(ip,port)
                        self.session.peer_socket = create_client(ip, port)
                        break
                if not self.session.peer_found:
                    return Panel(Text(f"{inp} is not online or nickname is incorrect.", style="red"), title="Error")
            else:
                self.session.messages.append(f"[bold red]You:[/bold red] {inp}")
                try:
                    self.session.peer_socket.send(inp.encode())
                except Exception as e:
                    self.session.messages.append(f"[red]Failed to send: {e}[/red]")
         if self.session.current_peer:
            chat_history = Text.from_markup("\n".join(self.session.messages))
            return Panel(chat_history, title=f"Chatting with {self.session.current_peer}", border_style="blue")
         else:
            return Panel(Text("Enter the nickname of the person you want to chat with"), title="Chat")



             


                 
             
             



