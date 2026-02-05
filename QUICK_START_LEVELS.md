# Quick Start: Level System

## What's New?

Terminal Trail now has a **7-level game structure** that organizes all 63 challenges into progressive learning levels, making the experience more game-like and motivating.

## Visual Changes

### Before
```
📚 Chapter 1: Home | 🎮 Challenge 1
```

### After
```
🌱 Level 1: First Steps | 🎮 Challenge 1 (1/6)
```

Now you can see:
- Which level you're on (with emoji!)
- Level name
- Your position within the level (1/6 means challenge 1 of 6)

## The 7 Levels

| Level | Name | Challenges | Commands |
|-------|------|------------|----------|
| 🌱 1 | First Steps | 1-6 (6) | ls, cat, cd |
| 🗺️ 2 | Navigation Mastery | 7-15 (9) | pwd, cd |
| 🔍 3 | Hidden Things | 16-22 (7) | ls -a |
| 📦 4 | Moving Things | 23-30 (8) | mv |
| 💬 5 | Speaking Up | 31-40 (10) | echo |
| 🎯 6 | Advanced Exploration | 41-50 (10) | all |
| ⚔️ 7 | The Power to Remove | 51-63 (13) | rm, chmod |

## Try It Out

### Terminal Version
```bash
python3 play.py
```

You'll see the level info at the top of each challenge!

### Web Version
```bash
python3 web_server.py
```

Visit `http://localhost:8000` and you'll see:
- A green badge in the header showing your current level
- Level info in the terminal output
- The badge updates as you progress!

## Test the System

```bash
# Run the test suite
python3 test_levels.py
```

This shows:
- All 7 levels with descriptions
- Challenge distribution
- Verification that all 63 challenges are mapped

## For Developers

### Get Level Info for Any Challenge
```python
from level_config import get_level_progress

# Get info for challenge 23
info = get_level_progress(23)
print(info)
# {
#   "level_num": 4,
#   "level_name": "Moving Things",
#   "level_emoji": "📦",
#   "level_description": "Moving files and directories around",
#   "challenge_position": 1,
#   "total_challenges": 8,
#   "progress_percent": 12
# }
```

### Level Configuration
Edit `level_config.py` to:
- Change level names or descriptions
- Adjust challenge groupings
- Modify emojis
- Add new levels

## Documentation

- **`LEVEL_STRUCTURE.md`** - Complete level guide with learning objectives
- **`LEVEL_SYSTEM_IMPLEMENTATION.md`** - Technical implementation details
- **`level_config.py`** - Level definitions and helper functions

## No Breaking Changes

- All existing challenges work exactly the same
- Progress files are automatically upgraded
- Chapter system still exists (for now)
- All game logic unchanged

## What's Next?

The level system is ready to use! Possible future enhancements:
- Level completion celebration screens
- Level selection menu
- Progress bars
- Achievements/badges
- Level replay functionality

Enjoy the new level system! 🎮
