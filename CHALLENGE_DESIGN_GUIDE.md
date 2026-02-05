# Challenge Design Guide

## Navigation Challenge Best Practices

### Problem
Navigation challenges were requiring exact command matches, making them frustrating when players used valid alternative paths (e.g., `cd ~/town` vs `cd ../town` vs `cd ..` then `cd town`).

### Solution
The game engine now automatically checks if the player has reached the `end_dir` after ANY `cd` command, regardless of the specific command used.

**Implementation:** See `game_engine.py` lines 296-299

```python
# Check if we've reached the end directory (for navigation challenges)
current_dir = self.terminal_handler.get_current_directory()
if end_dir != '~' and end_dir == current_dir and user_input.startswith('cd'):
    # Navigation challenge completed by reaching destination
    return True
```

---

## Challenge Format Guidelines

### 1. Pure Navigation Challenges
**Goal:** Player just needs to reach a destination

**Format:**
```json
{
  "objective": "Navigate to town",
  "start_dir": "~/my-house",
  "end_dir": "~/town",
  "commands": [],
  "hints": [
    "Use 'cd town' to go there",
    "Or use 'cd ~/town' for absolute path",
    "Or use 'cd ..' then 'cd town' step by step"
  ]
}
```

**Key Points:**
- ✅ `commands` is **empty** `[]`
- ✅ Set `start_dir` and `end_dir`
- ✅ Game automatically accepts ANY valid path
- ✅ Player can use: absolute paths, relative paths, step-by-step navigation

**Examples:**
- Challenge 15: Navigate home from town
- Challenge 16 Step 1: Navigate to town from house

---

### 2. Navigation + Action Challenges
**Goal:** Player needs to reach a destination AND perform an action

**Format:**
```json
{
  "objective": "Go to town and look around",
  "start_dir": "~/my-house",
  "end_dir": "~/town",
  "commands": ["ls"],
  "hints": [
    "First navigate to town using cd",
    "Then use 'ls' to look around"
  ]
}
```

**Key Points:**
- ✅ `commands` contains **only the action command** (not navigation)
- ✅ Navigation is handled automatically by destination checking
- ✅ Player must reach `end_dir` AND execute the action command

**Examples:**
- Challenge 16 Step 2: Go to town and use `ls`
- Challenge 16 Step 3: Stay in town and use `ls` again

---

### 3. Multi-Command Challenges
**Goal:** Player needs to execute multiple specific commands (not navigation)

**Format:**
```json
{
  "objective": "Talk to both the Mayor and Eleanor",
  "start_dir": "~/town",
  "end_dir": "~/town",
  "commands": [
    "cat Mayor",
    "cat Eleanor"
  ],
  "hints": [
    "Use 'cat Mayor' to talk to the Mayor",
    "Use 'cat Eleanor' to talk to Eleanor"
  ]
}
```

**Key Points:**
- ✅ List all required commands
- ✅ Game detects this as multi-command (2+ commands)
- ✅ Player must execute all listed commands
- ✅ Order doesn't matter (unless story requires it)

**Detection:** Game checks for patterns like "both", "all", "2 different", etc. in objective/story

---

### 4. Single Action Challenges
**Goal:** Player needs to execute one specific command

**Format:**
```json
{
  "objective": "Look around the room",
  "start_dir": "~/my-room",
  "end_dir": "~/my-room",
  "commands": ["ls"],
  "hints": [
    "Use 'ls' to look around"
  ]
}
```

**Key Points:**
- ✅ Single command in list
- ✅ `start_dir` and `end_dir` are the same (no navigation needed)
- ✅ Player must execute the exact command

---

## Common Patterns

### Pattern 1: Explore New Location
```json
{
  "story": ["You arrive at a new place..."],
  "objective": "Look around",
  "start_dir": "~/new-place",
  "end_dir": "~/new-place",
  "commands": ["ls"],
  "hints": ["Use 'ls' to see what's here"]
}
```

### Pattern 2: Navigate and Explore
```json
{
  "story": ["Go check out the town..."],
  "objective": "Go to town and look around",
  "start_dir": "~/my-house",
  "end_dir": "~/town",
  "commands": ["ls"],
  "hints": [
    "Navigate to town first",
    "Then use 'ls' to look around"
  ]
}
```

### Pattern 3: Talk to Character
```json
{
  "story": ["Find the Mayor..."],
  "objective": "Talk to the Mayor",
  "start_dir": "~/town",
  "end_dir": "~/town",
  "commands": ["cat Mayor"],
  "hints": ["Use 'cat Mayor' to talk to them"]
}
```

### Pattern 4: Navigate Home
```json
{
  "story": ["Time to go home..."],
  "objective": "Return home",
  "start_dir": "~/town",
  "end_dir": "~/my-house",
  "commands": [],
  "hints": [
    "Use 'cd ~/my-house' to go home",
    "Or navigate step by step"
  ]
}
```

---

## Troubleshooting

### Issue: Challenge requires exact command match
**Symptom:** Player types valid command but challenge doesn't complete

**Fix:** Check if it's a navigation challenge:
- If yes: Set `commands: []` and let destination checking handle it
- If no: Add all valid command variations to `commands` list

### Issue: Challenge says "X more commands to go"
**Symptom:** Game treats alternatives as multiple required commands

**Fix:** 
- For navigation: Use `commands: []`
- For actions: Only list the action commands, not navigation

### Issue: Player can't complete with alternative path
**Symptom:** `cd ~/town` works but `cd ../town` doesn't

**Fix:** This should be fixed by the game engine update. If not:
1. Check `game_engine.py` lines 296-299 exist
2. Verify `end_dir` is set correctly in challenge
3. Ensure `commands: []` for pure navigation

---

## Migration Checklist

When updating old navigation challenges:

- [ ] Check if challenge is pure navigation (just needs to reach destination)
- [ ] If yes, set `commands: []`
- [ ] Verify `start_dir` and `end_dir` are set correctly
- [ ] Update hints to mention multiple valid paths
- [ ] Test with different navigation methods:
  - [ ] Absolute path (`cd ~/destination`)
  - [ ] Relative path (`cd ../destination`)
  - [ ] Step by step (`cd ..` then `cd destination`)
- [ ] Verify challenge completes with all methods

---

## Examples of Fixed Challenges

### Challenge 15 (Before)
```json
{
  "commands": [
    "pwd",
    "cd ~/my-house",
    "cd ..",
    "cd ../my-house"
  ]
}
```
**Problem:** Required all 4 commands

### Challenge 15 (After)
```json
{
  "commands": []
}
```
**Solution:** Empty commands, destination checking handles it

### Challenge 16 Step 1 (Before)
```json
{
  "commands": [
    "cd town",
    "cd ~/town"
  ]
}
```
**Problem:** Treated as multi-command (need both)

### Challenge 16 Step 1 (After)
```json
{
  "commands": []
}
```
**Solution:** Empty commands, any path to `~/town` works

---

## Quick Reference

| Challenge Type | commands | start_dir | end_dir | Notes |
|---------------|----------|-----------|---------|-------|
| Pure Navigation | `[]` | Set | Set (different) | Any path works |
| Navigate + Action | `["action"]` | Set | Set | Navigation auto, then action |
| Multi-Command | `["cmd1", "cmd2"]` | Set | Set (same) | All commands required |
| Single Action | `["cmd"]` | Set | Set (same) | One specific command |

---

## Testing Navigation Challenges

Always test with these methods:

```bash
# Method 1: Absolute path
cd ~/destination

# Method 2: Relative path
cd ../destination

# Method 3: Step by step
cd ..
cd destination

# Method 4: Direct relative (if in parent)
cd destination
```

All should complete the challenge!

---

**Last Updated:** 2026-02-04
**Game Engine Version:** With automatic destination checking (game_engine.py lines 296-299)


---

## Modification Timing Best Practices

### Problem
Modifications are applied at the START of a step, BEFORE the player executes commands. This causes issues when modifications move files that the player is supposed to move.

### Solution
Place modifications in the step AFTER the player performs the action, to persist what they did.

### Pattern 1: Single Move Command

**WRONG:**
```json
{
  "step": 1,
  "objective": "Move apple into basket",
  "commands": ["mv apple basket"],
  "modifications": [
    {"action": "remove", "path": "~/apple"},
    {"action": "add", "path": "~/basket/apple"}
  ]
}
```
❌ Modifications move the apple BEFORE player can move it!

**CORRECT:**
```json
{
  "step": 1,
  "objective": "Move apple into basket",
  "commands": ["mv apple basket"],
  "next": [X, 2]
},
{
  "step": 2,
  "objective": "Check the apple is in basket",
  "commands": ["ls basket"],
  "modifications": [
    {"action": "remove", "path": "~/apple"},
    {"action": "add", "path": "~/basket/apple"}
  ],
  "next": [X, 3]
}
```
✅ Modifications persist what player did in previous step

### Pattern 2: Multi-Step Move Sequence

When an object moves multiple times across steps:

**Example:** Challenge 23 (apple in/out of basket)
```json
{
  "step": 1,
  "objective": "Move apple into basket",
  "commands": ["mv apple basket"],
  "next": [23, 2]
},
{
  "step": 2,
  "objective": "Check apple is gone",
  "commands": ["ls"],
  "modifications": [
    {"action": "remove", "path": "~/apple"},
    {"action": "add", "path": "~/basket/apple"}
  ],
  "next": [23, 3]
},
{
  "step": 3,
  "objective": "Check apple is in basket",
  "commands": ["ls basket"],
  "modifications": [
    {"action": "remove", "path": "~/apple"},
    {"action": "add", "path": "~/basket/apple"}
  ],
  "next": [23, 4]
},
{
  "step": 4,
  "objective": "Move apple back out",
  "commands": ["mv basket/apple ."],
  "next": [24, 1]
}
```

**Key Points:**
- Step 2 & 3: Repeat modifications to maintain state
- Step 4: No modifications (next challenge sets up its own state)
- Each step's modifications reflect CURRENT state, not future action

### Pattern 3: Cross-Challenge Persistence

When the next challenge needs files in a specific location:

**Example:** Challenge 23 → Challenge 24
```json
// Challenge 23, Step 4
{
  "objective": "Move apple back",
  "commands": ["mv basket/apple ."],
  "next": [24, 1]  // No modifications here
}

// Challenge 24, Step 1
{
  "story": ["Edith: 'Stop playing with that food!'"],
  "modifications": [
    {"action": "remove", "path": "~/basket/apple"},
    {"action": "add", "path": "~/apple"}  // Ensure apple is here
  ]
}
```

### Pattern 4: Multiple Files at Once

When moving multiple files in one step:

**Example:** Challenge 38 (moving animals to shelter)
```json
{
  "step": 6,
  "commands": ["mv Trotter .shelter/", "mv Daisy .shelter/", "mv Cobweb .shelter/", "mv Ruth .shelter/"],
  "modifications": [
    {"action": "remove", "path": "~/farm/barn/Trotter"},
    {"action": "remove", "path": "~/farm/barn/Daisy"},
    {"action": "remove", "path": "~/farm/barn/Cobweb"},
    {"action": "remove", "path": "~/farm/barn/Ruth"},
    {"action": "add", "path": "~/farm/barn/.shelter/Trotter", "type": "file", "content": "Trotter"},
    {"action": "add", "path": "~/farm/barn/.shelter/Daisy", "type": "file", "content": "Daisy"},
    {"action": "add", "path": "~/farm/barn/.shelter/Cobweb", "type": "file", "content": "Cobweb"},
    {"action": "add", "path": "~/farm/barn/.shelter/Ruth", "type": "file", "content": "Ruth"}
  ]
}
```

**Key Points:**
- All files must be explicitly listed in modifications
- Modifications persist ALL moves from that step

### Pattern 5: Wildcard Moves

When using wildcards like `mv cage/* ~/town`:
- Either add explicit modifications for each file
- Or ensure next challenge doesn't depend on those files being there
- Wildcard moves are complex - consider if they're necessary

---

## Fixed Challenges

The following challenges have been updated to follow these patterns:
- Challenge 23: Apple move sequence
- Challenge 24: Eleanor and dog rescue
- Challenge 38: Moving animals to shelter



---

## Command Alternatives Best Practice

### Problem
Many challenges list 4-8 command variations (e.g., `"mv basket ~", "mv basket/ ~", "mv basket ~/", "mv basket/ ~/"`) which creates confusion even though the game only requires 1.

### Solution
**List only 1-2 of the most common command variations.**

### Pattern

**WRONG (too many alternatives):**
```json
{
  "commands": [
    "mv basket ~",
    "mv basket/ ~",
    "mv basket ~/",
    "mv basket/ ~/",
    "mv basket ../..",
    "mv basket/ ../..",
    "mv basket ../../",
    "mv basket/ ../../"
  ]
}
```

**CORRECT (1-2 common alternatives):**
```json
{
  "commands": [
    "mv basket ~",
    "mv basket ~/"
  ]
}
```

### Game Logic
- If objective/story contains multi-command patterns ("at least 2", "everyone", "one by one"), game requires multiple commands
- Otherwise, `required_count = 1` - player only needs to complete ONE command from the list
- The commands array shows valid alternatives, not a checklist

### Recommendation
- **Single command**: List 1-2 variations (with/without trailing slash)
- **Navigation**: List 1-2 common paths (relative vs absolute)
- **Multi-command**: List all required commands (e.g., "move everyone")

