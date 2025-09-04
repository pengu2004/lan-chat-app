from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
import queue 

class ChatUI:
    def __init__(self,session):
        self.console = Console()
        self.session=session
        self.input_queue=queue.Queue()

    def onboarding(self): #to get the name of the current user and add it to the input queue
        self.console.print("[red]Welcome")
        name=self.console.input("What is [i]your[/i] [bold red]name[/]?  ")
        self.input_queue.put(name)
        
    


