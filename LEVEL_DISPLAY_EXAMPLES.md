# Level Display Examples

## What Players See

### Example 1: Starting the Game (Challenge 1)

```
============================================================
🎮 TERMINAL TRAIL - Learn Linux Commands Through Story 🎮
============================================================

Welcome to Terminal Trail! You'll learn Linux commands by
playing through an interactive story. Type the commands
exactly as shown to progress through the adventure.

💡 Tips:
  • Type 'help' for available commands
  • Type 'hint' if you're stuck
  • Type 'quit' to exit the game
  • Use TAB for auto-completion

Starting Challenge 1, Step 1
============================================================

🌱 Level 1: First Steps | 🎮 Challenge 1 (1/6)
============================================================

📖 STORY:
----------------------------------------
🔔 Alarm: "Beep beep beep! Beep beep beep!"

📻 Radio: "Good Morning, this is the 9am news."
"The town of Folderton has awoken to strange news..."
----------------------------------------

🎯 OBJECTIVE: Type 'ls' and press Enter to look around your bedroom

💻 TERMINAL (Current directory: ~/my-house/my-room)
Type your commands below:
~/my-house/my-room $
```

### Example 2: Mid-Level Progress (Challenge 4)

```
🌱 Level 1: First Steps | 🎮 Challenge 4 (4/6)
============================================================

📖 STORY:
----------------------------------------
You're exploring your room and learning the basics...
----------------------------------------

🎯 OBJECTIVE: Use 'cat' to read the note

💻 TERMINAL (Current directory: ~/my-house/my-room)
```

### Example 3: Starting a New Level (Challenge 7)

```
🗺️ Level 2: Navigation Mastery | 🎮 Challenge 7 (1/9)
============================================================

📖 STORY:
----------------------------------------
👩 Mum: "Hi sleepyhead, breakfast is nearly ready. 
Can you go and grab your Dad? I think he's in the garden."

Let's look for your Dad in the garden.
First we need to leave the kitchen using 'cd ..'
----------------------------------------

🎯 OBJECTIVE: Leave the kitchen

💻 TERMINAL (Current directory: ~/my-house/kitchen)
```

### Example 4: Mid-Game (Challenge 23)

```
📦 Level 4: Moving Things | 🎮 Challenge 23 (1/8)
============================================================

📖 STORY:
----------------------------------------
Now you'll learn to move files and directories!
This is a powerful command that lets you organize things.
----------------------------------------

🎯 OBJECTIVE: Move the file to the destination

💻 TERMINAL (Current directory: ~/town)
```

### Example 5: Advanced Level (Challenge 41)

```
🎯 Level 6: Advanced Exploration | 🎮 Challenge 41 (1/10)
============================================================

📖 STORY:
----------------------------------------
You've learned many commands. Now it's time to combine them
and solve more complex challenges!
----------------------------------------

🎯 OBJECTIVE: Navigate to the library and find the hidden scroll

💻 TERMINAL (Current directory: ~/town)
```

### Example 6: Final Level (Challenge 51)

```
⚔️ Level 7: The Power to Remove | 🎮 Challenge 51 (1/13)
============================================================

📖 STORY:
----------------------------------------
You've reached the final level! Here you'll learn the most
powerful command - the ability to remove files.
Use it wisely!
----------------------------------------

🎯 OBJECTIVE: Enter the cave system

💻 TERMINAL (Current directory: ~/woods)
```

### Example 7: Last Challenge (Challenge 63)

```
⚔️ Level 7: The Power to Remove | 🎮 Challenge 63 (13/13)
============================================================

📖 STORY:
----------------------------------------
This is it - the final challenge! You've learned all the
essential Linux commands. Time to complete your quest!
----------------------------------------

🎯 OBJECTIVE: Complete the final task

💻 TERMINAL (Current directory: ~/cave)
```

## Web Interface Display

### Header Badge
```
┌─────────────────────────────────────────┐
│        🎮 Terminal Trail                │
│   Learn Linux Commands Through Story    │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Level 1: First Steps             │ │  ← Green badge
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

The badge updates automatically as you progress:
- Challenge 1-6: `Level 1: First Steps`
- Challenge 7-15: `Level 2: Navigation Mastery`
- Challenge 16-22: `Level 3: Hidden Things`
- Challenge 23-30: `Level 4: Moving Things`
- Challenge 31-40: `Level 5: Speaking Up`
- Challenge 41-50: `Level 6: Advanced Exploration`
- Challenge 51-63: `Level 7: The Power to Remove`

## Progress Indicators

### Within a Level
- `(1/6)` - Just started the level
- `(3/6)` - Halfway through
- `(6/6)` - Last challenge of the level

### Level Completion
When you complete challenge 6, you'll see:
```
✅ Challenge completed! Moving to next step...
Press Enter to continue...

🗺️ Level 2: Navigation Mastery | 🎮 Challenge 7 (1/9)
```

Notice the level changed from 🌱 to 🗺️!

## Saved Progress Display

When resuming:
```
============================================================
📁 Saved progress found!
   Challenge 23, Step 1
   Level 4: Moving Things
============================================================

Would you like to resume from where you left off? (y/n):
```

## Level Emojis at a Glance

- 🌱 = Beginner (First Steps)
- 🗺️ = Navigation (Navigation Mastery)
- 🔍 = Discovery (Hidden Things)
- 📦 = Organization (Moving Things)
- 💬 = Communication (Speaking Up)
- 🎯 = Mastery (Advanced Exploration)
- ⚔️ = Power (The Power to Remove)

## Benefits of This Display

1. **Clear Progress**: See exactly where you are (3/6)
2. **Motivation**: Watch the numbers increase
3. **Context**: Know which level you're in
4. **Achievement**: Feel accomplished when reaching new levels
5. **Visual Appeal**: Emojis make it more engaging
6. **Information Density**: All key info in one line

The level system makes Terminal Trail feel more like a game while maintaining its educational focus!
