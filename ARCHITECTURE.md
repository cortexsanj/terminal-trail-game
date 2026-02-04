# Terminal Trail - Simplified Architecture

## Overview

Terminal Trail Simplified is a clean, terminal-only implementation of the Linux command learning game. It focuses on the core educational experience without GUI complexity.

## Architecture Components

### 1. Game Engine (`game_engine.py`)
**Purpose**: Main game orchestrator and loop controller

**Key Features**:
- Manages game state (current challenge/step)
- Coordinates all other components
- Handles user interaction flow
- Saves/loads progress
- Displays story content and manages challenge progression

**Main Methods**:
- `start()` - Initialize and begin game
- `_game_loop()` - Main game execution loop
- `_run_challenge()` - Execute individual challenge
- `_check_command_success()` - Validate user commands

### 2. Story Manager (`story_manager.py`)
**Purpose**: Handles story content and challenge definitions

**Key Features**:
- Loads challenge data from JSON files
- Manages story text and objectives
- Loads ASCII art from story files
- Auto-generates challenge files on first run

**Data Structure**:
```json
{
  "title": "Challenge Title",
  "description": "What this teaches",
  "commands_taught": ["ls", "cd"],
  "steps": [
    {
      "story": ["Story text lines..."],
      "objective": "What player needs to do",
      "commands": ["required command"],
      "hints": ["Help text..."],
      "next": [next_challenge, next_step]
    }
  ]
}
```

### 3. Terminal Handler (`terminal_handler.py`)
**Purpose**: Processes and executes terminal commands

**Key Features**:
- Command parsing and validation
- Real command execution simulation
- Directory navigation tracking
- Output formatting and error handling

**Supported Commands**:
- `ls` - List directory contents
- `cd` - Change directories
- `cat` - Display file contents
- `pwd` - Show current directory
- `mkdir` - Create directories
- `echo` - Print text / create files
- `mv` - Move/rename files
- `rm` - Remove files

### 4. File System (`file_system.py`)
**Purpose**: Virtual file system for the game world

**Key Features**:
- Hierarchical directory structure
- Dynamic file/directory creation
- Story file content loading
- Path resolution and navigation

**Structure**:
```
~/
├── my-house/
│   ├── my-room/
│   │   ├── alarm (file)
│   │   ├── bed (file)
│   │   ├── wardrobe/
│   │   │   ├── t-shirt (file)
│   │   │   ├── trousers (file)
│   │   │   └── cap (file)
│   │   └── shelves/
│   │       ├── comic-book (file)
│   │       └── note (file)
│   ├── kitchen/
│   ├── parents-room/
│   └── garden/
```

### 5. Progress Tracker (`progress_tracker.py`)
**Purpose**: Saves and loads game progress

**Key Features**:
- JSON-based progress storage
- Challenge completion tracking
- Resume functionality
- Progress statistics

## Game Flow

1. **Initialization**
   - Load saved progress (if any)
   - Initialize file system
   - Setup terminal handler

2. **Challenge Loop**
   - Load challenge data
   - Setup file system for challenge
   - Display story text and objective
   - Accept user commands
   - Validate command success
   - Progress to next challenge/step

3. **Command Processing**
   - Parse user input
   - Execute command in virtual file system
   - Return output and success status
   - Check against challenge requirements

## Key Design Decisions

### Simplicity First
- No GUI dependencies
- Pure terminal interface
- Minimal external dependencies
- Clean, readable code structure

### Educational Focus
- Progressive command introduction
- Story-driven learning context
- Immediate feedback and hints
- Real command behavior simulation

### Extensibility
- JSON-based challenge definitions
- Modular component architecture
- Easy to add new commands
- Simple to create new challenges

## File Structure

```
terminal_quest_simple/
├── main.py              # Entry point
├── game_engine.py       # Main game logic
├── story_manager.py     # Story and challenge management
├── terminal_handler.py  # Command processing
├── file_system.py       # Virtual file system
├── progress_tracker.py  # Save/load progress
├── test_game.py         # Test suite
├── challenges/          # Generated challenge files
├── assets/              # Story files and ASCII art
│   └── story_files/     # Individual story assets
├── README.md            # User documentation
└── ARCHITECTURE.md      # This file
```

## Advantages Over Original

1. **Simplified Dependencies**: No GTK, no Kano OS dependencies
2. **Cross-Platform**: Works on any system with Python 3
3. **Maintainable**: Clean, modular architecture
4. **Extensible**: Easy to add new challenges and commands
5. **Focused**: Pure terminal learning experience
6. **Lightweight**: Minimal resource usage

## Future Enhancements

1. **More Commands**: Add `grep`, `find`, `chmod`, `sudo`
2. **More Challenges**: Expand to 25+ challenges
3. **Better Hints**: Context-aware help system
4. **Tab Completion**: Real terminal-like autocomplete
5. **Command History**: Up/down arrow navigation
6. **Scripting**: Teach shell scripting concepts
7. **Multiplayer**: Shared learning sessions

## Testing

Run the test suite:
```bash
python3 test_game.py
```

This validates:
- All components work correctly
- File system operations
- Command execution
- Story loading
- Challenge progression