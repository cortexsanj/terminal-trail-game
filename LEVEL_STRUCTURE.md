# Terminal Trail - Level Structure

Terminal Trail now features a game-like level structure that organizes the 63 challenges into 7 progressive levels. Each level introduces new commands and builds upon previous knowledge.

## Hierarchy

```
LEVEL > CHALLENGE > STEP
```

- **Level**: A thematic grouping of challenges (7 total)
- **Challenge**: A specific learning objective (63 total)
- **Step**: Individual actions within a challenge (varies per challenge)

## The 7 Levels

### 🌱 Level 1: First Steps (Challenges 1-6)
**Commands**: `ls`, `cat`, `cd`

Learn the basics of navigation and examining objects. Wake up to mysterious news and start exploring your room and house.

**Learning Goals**:
- Basic navigation with `cd`
- Examining objects with `cat`
- Looking around with `ls`
- Understanding directories

---

### 🗺️ Level 2: Navigation Mastery (Challenges 7-15)
**Commands**: `pwd`, advanced `cd`

Master multi-level navigation and understand file system paths. Journey from your house to town while learning about the mysterious events.

**Learning Goals**:
- Multi-level navigation
- Understanding paths (relative and absolute)
- Using `pwd` for location awareness
- Using `cd ~` to return home

---

### 🔍 Level 3: Hidden Things (Challenges 16-22)
**Commands**: `ls -a`

Discover hidden files and directories as the mystery deepens. Learn to see what's normally invisible.

**Learning Goals**:
- Discovering hidden files with `ls -a`
- Understanding dot-prefixed items
- Finding secret information
- Exploring hidden directories

---

### 📦 Level 4: Moving Things (Challenges 23-30)
**Commands**: `mv`

Learn to move and organize files. Help rescue survivors and gather supplies using the `mv` command.

**Learning Goals**:
- Moving files with `mv`
- Moving directories
- Understanding source and destination paths
- Using `.` and `..` in paths
- Renaming files

---

### 💬 Level 5: Speaking Up (Challenges 31-40)
**Commands**: `echo`

Use `echo` to communicate and make choices. Explore ancient scrolls and meet new characters.

**Learning Goals**:
- Using `echo` for output
- Interactive dialogue choices
- Combining commands with navigation
- Story-driven command usage

---

### 🎯 Level 6: Advanced Exploration (Challenges 41-50)
**Commands**: All previous commands combined

Put all your skills together in complex scenarios. Explore the library, solve riddles, and uncover secrets.

**Learning Goals**:
- Combining all learned commands
- Problem-solving with multiple commands
- Complex navigation scenarios
- Riddle solving

---

### ⚔️ Level 7: The Power to Remove (Challenges 51-63)
**Commands**: `rm`, `chmod` (permissions)

Master the power to remove files and understand permissions. Complete your quest and face the final confrontation.

**Learning Goals**:
- Using `rm` to remove files
- Understanding file permissions
- Careful use of destructive commands
- Completing the quest

---

## Display Format

### In Terminal
```
🌱 Level 1: First Steps | 🎮 Challenge 1 (1/6)
```

### In Web Interface
The level is shown both:
1. In the header as a badge: `Level 1: First Steps`
2. In the terminal output with the challenge info

## Progress Tracking

Progress is saved with level information:
```json
{
  "challenge": 7,
  "step": 1,
  "level": 2,
  "level_name": "Navigation Mastery",
  "completed_challenges": [1, 2, 3, 4, 5, 6]
}
```

## Implementation Files

- `level_config.py` - Level definitions and helper functions
- `progress_tracker.py` - Updated to track level progress
- `game_engine.py` - Updated to display level info
- `web_server.py` - Updated web interface with level display
- `web_static/` - HTML/CSS/JS with level indicator

## Benefits

1. **Clear Progression**: Players see their progress through levels
2. **Motivation**: Level completion provides achievement milestones
3. **Organization**: Commands are grouped by learning objectives
4. **Pacing**: Natural breaks between levels for online modules
5. **Game-like Feel**: More engaging than just numbered challenges
