import time
from discovery import PeerDiscovery
from ui import ChatUI
from chat_session import ChatSession
from rich.live import Live
from rich.console import Group
from network import start_server

def main():
    print("Starting LAN Chat App...")

    # Get user nickname
    chat_session = ChatSession()
    chat_session.my_name = input("Enter your nickname: ").strip()

    # Start discovery
    discovery = PeerDiscovery(chat_session.my_name)
    discovery.start()

    # Share peerlist with session for UI access
    chat_session.peerlist = discovery.peerlist
    start_server(chat_session.peerlist)


    # Create UI instance
    chat_ui = ChatUI(chat_session)

    # Rich Live for dynamic updates
    with Live(refresh_per_second=10, screen=True) as live:
        while True:
            # Generate UI components
            peerlist_table = chat_ui.generate_table()
            user_panel = chat_ui.display_name()
            chat_panel = chat_ui.chat_box()

            # Group components for proper rendering
            layout = Group(
                peerlist_table,
                user_panel,
                chat_panel
            )

            # Update the live display
            live.update(layout)

            # Brief sleep to reduce CPU load
            time.sleep(0.1)

if __name__ == "__main__":
    main()
