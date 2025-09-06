# LAN Chat App

A real-time peer-to-peer chat application for Local Area Networks (LAN) built with Python. This application enables instant messaging between devices on the same network without requiring a central server.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-Open_Source-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)

## ✨ Features

- **🔍 Automatic Peer Discovery**: Automatically finds other chat app instances on your local network
- **💬 Real-time Messaging**: Instant messaging with live UI updates
- **🖥️ Rich Terminal Interface**: Beautiful, responsive terminal UI using Rich library
- **👥 Multi-peer Support**: Connect and chat with multiple users simultaneously
- **🔄 Auto-cleanup**: Automatically removes inactive peers from the list
- **🌐 Cross-platform**: Works on Linux, Windows, and macOS
- **⚡ Zero Configuration**: No server setup required - just run and chat!

## 📋 Prerequisites

- Python 3.7 or higher
- Rich library for terminal UI
- Network access (same LAN/WiFi network)

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pengu2004/lan-chat-app.git
   cd lan-chat-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install rich
   ```

### Running the Application

1. **Start the application**
   ```bash
   python3 main.py
   ```
   
2. **Enter your name** when prompted
   ```
   Hii Welcome
   What is your name? YourName
   ```

3. **Wait for peers to appear** in the left panel (may take up to 10 seconds)

4. **Start chatting** by typing a peer's nickname in the chat area

## 📖 How to Use

### Starting a Chat

1. **Launch the app** on multiple devices in your network
2. **Wait for peer discovery** - other users will appear in the "Peerlist" on the left
3. **Select a peer** by typing their exact nickname in the chat area
4. **Start messaging** - type your message and press Enter

### Interface Layout

```
┌─────────────┐┌──────────────────────────────────┐
│  Peerlist   ││          Your Name               │
│             │├──────────────────────────────────┤
│ IP:Port     ││                                  │
│ Nickname    ││         Chat Area                │
│ Ping        ││                                  │
│             ││  Type nickname to connect        │
│             ││  Type messages to send           │
│             ││                                  │
└─────────────┘└──────────────────────────────────┘
```

### Example Chat Session

```
# Device 1 - Alice
What is your name? Alice

# Device 2 - Bob  
What is your name? Bob

# Alice's interface shows:
Peerlist:
192.168.1.100:7777 | Bob | 1.2

# Alice types "Bob" to connect, then messages:
Alice: Hi Bob!
Bob: Hello Alice! How are you?
Alice: Great! This LAN chat is working perfectly!
```

## ⚙️ Configuration

The application uses a configuration class located in `configs.py`. You can modify these settings:

```python
class Config:
    BROADCAST_PORT = 50001        # UDP port for peer discovery
    BROADCAST_INTERVAL = 3        # Seconds between discovery broadcasts
    WAIT_TIME = 10               # Seconds before removing inactive peers
    SERVER_PORT = 7777           # TCP port for chat connections
    REFRESH_RATE = 4             # UI refresh rate per second
    UI_UPDATE_INTERVAL = 0.4     # UI update interval in seconds
```

### Common Configuration Changes

- **Change chat port**: Modify `SERVER_PORT` if port 7777 is in use
- **Adjust peer timeout**: Increase `WAIT_TIME` for slower networks
- **Discovery frequency**: Modify `BROADCAST_INTERVAL` (lower = more frequent discovery)

## 🏗️ Architecture

The application follows a clean, class-based architecture:

### Core Components

- **`ChatApplication`** (`main.py`) - Main application controller
- **`PeerDiscovery`** (`discovery.py`) - UDP-based peer discovery system
- **`NetworkManager`** (`network.py`) - TCP connection and message handling
- **`DisplayManager`** (`display_mod.py`) - Rich-based terminal UI
- **`Config`** (`configs.py`) - Centralized configuration management

### Communication Flow

```
┌─────────────────┐    UDP Broadcast    ┌─────────────────┐
│     Device A    │◄─────────────────────┤     Device B    │
│   (Discovery)   │─────────────────────►│   (Discovery)   │
└─────────────────┘                     └─────────────────┘
         │                                         │
         │            TCP Connection               │
         │◄───────────────────────────────────────►│
         │             (Chat Messages)             │
```

### Threading Model

- **Main Thread**: UI rendering and updates
- **Discovery Broadcaster**: Sends periodic UDP broadcasts
- **Discovery Listener**: Listens for peer announcements
- **Peer Cleanup**: Removes inactive peers
- **Chat Server**: Accepts incoming connections
- **Message Handler**: Processes incoming messages
- **Input Handler**: Non-blocking user input

For detailed architecture information, see [README_Refactoring.md](README_Refactoring.md).

## 🔧 Troubleshooting

### Common Issues

#### "Operation not permitted" Error
```
PermissionError: [Errno 1] Operation not permitted
```
- **Cause**: Network permissions or firewall blocking UDP broadcast
- **Solution**: 
  - Run as administrator/sudo (not recommended for security)
  - Check firewall settings for UDP port 50001
  - Ensure you're on the same network segment

#### No Peers Appearing
- **Check network connectivity**: Ensure devices are on the same LAN/WiFi
- **Wait longer**: Peer discovery can take up to 10 seconds
- **Check firewall**: Both UDP (50001) and TCP (7777) ports need to be open
- **Network isolation**: Some networks isolate devices (guest networks, etc.)

#### Connection Refused
```
ConnectionRefusedError: [Errno 111] Connection refused
```
- **Solution**: Ensure the target device is running the chat application
- **Check ports**: Verify TCP port 7777 is not blocked

#### Chat Messages Not Sending
- **Verify connection**: Check that you've successfully connected to a peer
- **Network issues**: Check for network connectivity problems
- **Restart app**: Sometimes reconnection is needed

### Network Requirements

- **Ports Used**:
  - UDP 50001: Peer discovery
  - TCP 7777: Chat messages
- **Network Type**: Same subnet/LAN required
- **Firewall**: Must allow traffic on both ports

## 🛠️ Development

### Project Structure

```
lan-chat-app/
├── main.py              # Application entry point
├── configs.py           # Configuration settings
├── discovery.py         # Peer discovery logic
├── network.py           # Network communication
├── display_mod.py       # UI and display management
├── requirements.txt     # Python dependencies
├── README.md           # Main documentation (this file)
├── README_Refactoring.md # Technical architecture details
└── .gitignore          # Git ignore rules
```

### Running in Development Mode

1. **Clone and setup**
   ```bash
   git clone https://github.com/pengu2004/lan-chat-app.git
   cd lan-chat-app
   pip install -r requirements.txt
   ```

2. **Test locally** (requires multiple terminals or devices)
   ```bash
   # Terminal 1
   python3 main.py
   
   # Terminal 2 (different device preferred)
   python3 main.py
   ```

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Maintain class-based architecture
- Keep configuration centralized in `configs.py`

### Testing

Currently, the application requires manual testing with multiple instances. To test:

1. Run application on 2+ devices/terminals
2. Verify peer discovery works
3. Test message sending/receiving
4. Check cleanup of inactive peers

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/new-feature`)
3. **Make your changes** following the existing code style
4. **Test thoroughly** with multiple instances
5. **Commit your changes** (`git commit -am 'Add new feature'`)
6. **Push to the branch** (`git push origin feature/new-feature`)
7. **Create a Pull Request**

### Areas for Contribution

- **GUI Interface**: Desktop GUI using tkinter/PyQt
- **File Transfer**: Add file sharing capabilities
- **Encryption**: Add message encryption for security
- **Group Chats**: Support for group messaging
- **Message History**: Persistent chat history
- **Notifications**: System notifications for new messages
- **Mobile Support**: Mobile-friendly version

## 📚 Technical Details

For in-depth technical information about the refactoring process and class-based architecture, see [README_Refactoring.md](README_Refactoring.md).

## 🔄 Changelog

### Latest Version
- ✅ Complete class-based refactoring
- ✅ Clean architecture with separation of concerns
- ✅ Improved maintainability and testability
- ✅ Rich terminal UI with live updates
- ✅ Cross-platform compatibility

## 📄 License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## 🙋‍♂️ Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [Technical Details](README_Refactoring.md)
3. Open an issue on GitHub
4. Check that you're following the setup instructions exactly

---

**Made with ❤️ for local network communication**

*Happy chatting on your LAN!* 🚀