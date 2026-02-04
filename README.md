# Terminal Trail - Simplified Edition

A streamlined, terminal-only version of Terminal Trail that teaches Linux commands through an interactive story.

## Features

- **Pure Terminal Experience** - No GUI, just command line learning
- **Progressive Story** - Learn commands through engaging narrative with characters and mystery
- **Real Command Execution** - Practice actual Linux commands in a safe environment
- **Cross-Platform** - Works on macOS, Linux, and other Unix systems
- **Zero Dependencies** - Only Python 3.6+ standard library required
- **Complete Adventure** - 63 challenges with 250+ steps teaching 12 essential commands

## Quick Start

```bash
cd terminal_quest_simple
python3 main.py
```

## Game Content

### Story Overview
You wake up to mysterious news about missing people in the town of Folderton. As you explore your house, town, woods, and mysterious caves, you learn Linux commands while uncovering a dark plot involving a cursed Rabbit and a magical bell. The game combines learning with an engaging mystery narrative that takes you from beginner to hero.

### Complete Challenge List (63 Total)

#### Chapter 1: Home (Challenges 1-10)
Wake up, explore your house, meet your family, and learn basic navigation.
- Commands: `ls`, `cat`, `cd`, `pwd`

#### Chapter 2: Town (Challenges 11-20)
Venture into town, meet the townspeople, and learn file management.
- Commands: `mkdir`, `echo`, `mv`

#### Chapter 3: Woods (Challenges 21-30)
Explore the woods, solve puzzles, and master advanced navigation.
- Commands: Advanced `cd`, `mv`, file organization

#### Chapter 4: Cave (Challenges 31-40)
Enter mysterious caves, learn text editing, and run scripts.
- Commands: `vi`, shell scripts

#### Chapter 5: Permissions (Challenges 41-57)
Master file permissions, unlock secrets, and prepare for the finale.
- Commands: `chmod`, `ls -l`, permission management

#### Chapter 6: Finale (Challenges 58-63)
Confront the Rabbit, save the townspeople, and become a hero!
- Commands: `rm`, `sudo`, wildcards

### Characters & Locations
- **Characters**: Mum, Dad, Mayor, Bernard, Eleanor, Edward, Ruth, Edith, Swordmaster, Rabbit, and more
- **Locations**: Your house, town square, library, woods, caves, rabbithole, and secret areas
- **Items**: 100+ interactive objects and story files
- **Story Elements**: Missing people mystery, cursed Rabbit, magical bell, ancient scrolls

## Architecture

- `main.py` - Entry point and game launcher
- `game_engine.py` - Core game loop and challenge management
- `terminal_handler.py` - Command processing and validation
- `story_manager.py` - Story text and narrative management
- `file_system.py` - Game world file system management
- `challenges/` - Individual challenge definitions (auto-generated)
- `assets/` - Story files and ASCII art (200+ files)
- `data/` - Game world structure definitions

## Commands Taught

### Navigation & Exploration
1. `ls` - List files and directories
2. `ls -a` - List including hidden files
3. `ls -l` - Long format with permissions
4. `cd` - Change directories  
5. `pwd` - Show current directory
6. `cat` - View file contents

### File & Directory Management
7. `mkdir` - Create directories
8. `mv` - Move/rename files (with wildcard support)
9. `rm` - Remove files
10. `echo` - Print text and create files

### Advanced Operations
11. `vi` - Text editor for file editing
12. `chmod` - Change file permissions (+r, +w, +x, +rwx)
13. `sudo` - Execute commands as super user
14. `./script.sh` - Run shell scripts

## Game Experience

### Educational Design
- **Story-Driven Learning** - Commands taught through narrative context
- **Progressive Difficulty** - Each challenge builds on previous knowledge
- **Immediate Feedback** - Real-time validation and hints
- **Character Interactions** - Learn by talking to townspeople
- **Mystery Elements** - Engaging plot keeps players motivated
- **Complete Arc** - From beginner to hero in 63 challenges

### Interactive Features
- **250+ Steps** - Detailed exploration of each command
- **15+ Characters** - Rich interactions with townspeople
- **Environmental Storytelling** - Discover the story through exploration
- **Contextual Hints** - Help that makes sense for the situation
- **Progress Tracking** - Save and resume your adventure
- **Multiple Locations** - 20+ unique areas to explore

## Comparison with Original

| Aspect | Original Game | Simplified Version |
|--------|---------------|-------------------|
| **Dependencies** | GTK3, PyGObject, pygame | Python 3.6+ only |
| **Interface** | GUI with terminal emulator | Pure terminal |
| **Challenges** | 63 challenges | 63 challenges (complete) |
| **Commands** | 12+ commands | 12 essential commands |
| **Story** | Full narrative | Complete story maintained |
| **Characters** | 15+ NPCs | All characters included |
| **Learning** | Story-integrated | Story-integrated |
| **Platform** | Linux-focused | Cross-platform |
| **Complexity** | Complex codebase | Clean, maintainable |

## What's Included

### ✅ Complete Story
- **Full Narrative** - All 63 challenges from original game
- **Character Development** - Meet townspeople, solve mysteries
- **Mystery Plot** - Cursed Rabbit, missing people, magical bell
- **Progressive Revelation** - Story unfolds as you learn commands
- **Satisfying Conclusion** - Save the town and become a hero

### ✅ All Essential Commands  
- **12 Commands** - All core Linux commands from original
- **Real Syntax** - Actual command-line syntax and behavior
- **Practical Skills** - Commands you'll use in real systems
- **Progressive Learning** - From basic to advanced operations

### ✅ Educational Excellence
- **Gradual Introduction** - Commands introduced when story needs them
- **Repeated Practice** - Multiple opportunities to use each command
- **Real-World Context** - Commands used for actual story purposes
- **Meaningful Feedback** - Hints and responses tied to story situation
- **Skill Building** - Each challenge builds on previous knowledge

## Ready for Production

### Tested and Validated
- ✅ All 63 challenges implemented and tested
- ✅ Complete story progression verified
- ✅ All character interactions working
- ✅ File system includes all needed story assets
- ✅ Cross-platform compatibility maintained
- ✅ Zero external dependencies

### Complete Experience
- ✅ 250+ individual learning steps
- ✅ Rich story with mystery and adventure
- ✅ 15+ character interactions and dialogue
- ✅ Progressive skill building from beginner to advanced
- ✅ Engaging narrative that motivates learning
- ✅ Satisfying conclusion with hero's journey

The simplified Terminal Trail provides the complete learning experience of the original game while maintaining a clean, dependency-free architecture that runs anywhere Python 3.6+ is available.