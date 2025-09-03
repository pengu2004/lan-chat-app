import socket
import threading
import time
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from display_mod import generate_table,display_name,chat_box
from discovery import im_alive,are_you_there,cleaner


console=Console()

peerlist={}
peer_lock = threading.Lock() 



if __name__== "__main__":
    console.print("Hii Welcome",style="bold red")
    name=console.input("What is [i]your[/i] [bold red]name[/]?  ")


    im_alive_thread = threading.Thread(target=im_alive,args=(peerlist,name))
    are_you_there_thread = threading.Thread(target=are_you_there, args=(peerlist,peer_lock,name))
    cleaner_thread=threading.Thread(target=cleaner,args=(peerlist,peer_lock))

    im_alive_thread.start()
    are_you_there_thread.start()
    cleaner_thread.start()

    #main part of  display 
    #dividing the screen into 2 parts
    layout = Layout(name="root")
    layout.split_row(
        Layout(name="left"),
        Layout(name="right", ratio=3)
    )
    layout["right"].split_column(
        Layout(name="right_header", size=3), # A small top section for  name
        Layout(name="right_body")            
    )
    time.sleep(1) # Give the server a moment to start

    with Live(layout, refresh_per_second=4) as live:
        while True:
            layout["left"].update(generate_table(peerlist))
            layout["right_header"].update(display_name(name))
            layout["right_body"].update(chat_box(peerlist))
            
            live.update(layout)
            time.sleep(0.4)











