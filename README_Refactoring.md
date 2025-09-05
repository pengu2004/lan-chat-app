# LAN Chat App - Class-Based Refactoring

## Overview
This LAN Chat Application has been successfully refactored from a functional programming style to a clean, class-based architecture. The refactoring improves code organization, maintainability, and follows object-oriented design principles.

## Architecture

### Class Structure

1. **Config Class** (`configs.py`)
   - Centralized configuration management
   - All constants and settings in one place
   - Easy to modify and extend

2. **PeerDiscovery Class** (`discovery.py`)
   - Handles peer discovery and management
   - Manages peer list with thread-safe operations
   - Broadcasting, listening, and cleanup functionality

3. **NetworkManager Class** (`network.py`)
   - Handles all network communications
   - Server and client connection management
   - Message handling and socket operations

4. **DisplayManager Class** (`display_mod.py`)
   - Manages UI display using Rich library
   - Handles user input in a non-blocking way
   - Chat interface and peer list display

5. **ChatApplication Class** (`main.py`)
   - Main application controller
   - Orchestrates all components
   - Manages application lifecycle

## Key Improvements

### Before (Functional Style)
- Global variables scattered across modules
- Functions not logically grouped
- Tight coupling between modules
- Difficult to test individual components
- Hard to extend or modify

### After (Class-Based)
- Encapsulated related data and methods
- Clear separation of concerns
- Reduced global state
- Better maintainability and testability
- Easier to extend and modify

## Usage

### Class-Based Approach (Recommended)
```python
from main import ChatApplication

# Create and run the application
app = ChatApplication()
app.run()
```

### Direct Class Usage
```python
from configs import Config
from discovery import PeerDiscovery
from network import NetworkManager
from display_mod import DisplayManager

# Initialize components
discovery = PeerDiscovery("username")
network = NetworkManager(discovery.peerlist)
display = DisplayManager(network)

# Start services
discovery.start_discovery()
network.start_server()
```

## Benefits of the Refactoring

1. **Better Organization**: Related functionality is grouped together in classes
2. **Reduced Global State**: Data is encapsulated within appropriate classes
3. **Improved Testability**: Each class can be tested independently
4. **Enhanced Maintainability**: Changes are localized to specific classes
5. **Easier Extension**: New features can be added by extending existing classes
6. **Clear Dependencies**: Relationships between components are explicit

## Running the Application

```bash
python3 main.py
```

The application maintains all original functionality while providing a much cleaner and more maintainable codebase.