"""
Story Manager
Handles loading and managing story content and challenges
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional


class StoryManager:
    """Manages story content and challenge definitions"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.base_dir = Path(__file__).parent
        self.challenges_dir = self.base_dir / "challenges"
        self.assets_dir = self.base_dir / "assets" / "story_files"
        
        # Ensure directories exist
        self.challenges_dir.mkdir(exist_ok=True)
        
        # Initialize challenges if they don't exist
        self._initialize_challenges()
    
    def load_challenge(self, challenge_num: int, step_num: int) -> Optional[Dict]:
        """Load challenge data for specified challenge and step"""
        challenge_file = self.challenges_dir / f"challenge_{challenge_num:02d}.json"
        
        if not challenge_file.exists():
            return None
        
        try:
            with open(challenge_file, 'r') as f:
                challenge_data = json.load(f)
            
            # Get specific step
            steps = challenge_data.get('steps', [])
            if step_num <= len(steps):
                step_data = steps[step_num - 1]
                # Merge challenge-level data with step data
                result = {**challenge_data}
                result.update(step_data)
                return result
            
            return None
            
        except Exception as e:
            if self.debug:
                print(f"Error loading challenge {challenge_num}, step {step_num}: {e}")
            return None
    
    def load_story_file(self, filename: str) -> str:
        """Load content from a story file"""
        file_path = self.assets_dir / filename
        
        if not file_path.exists():
            return f"[Story file '{filename}' not found]"
        
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            if self.debug:
                print(f"Error loading story file {filename}: {e}")
            return f"[Error loading '{filename}']"
    
    def _initialize_challenges(self):
        """Initialize challenge files if they don't exist"""
        # Only create if challenges directory is empty
        if any(self.challenges_dir.glob("challenge_*.json")):
            return
        
        print("Initializing challenges...")
        
        # Create the first few essential challenges
        challenges = self._get_default_challenges()
        
        for i, challenge in enumerate(challenges, 1):
            challenge_file = self.challenges_dir / f"challenge_{i:02d}.json"
            with open(challenge_file, 'w') as f:
                json.dump(challenge, f, indent=2)
        
        print(f"Created {len(challenges)} challenges")
    
    def _get_default_challenges(self) -> List[Dict]:
        """Get default challenge definitions"""
        return [
            # Challenge 1: Introduction to ls
            {
                "title": "Wake Up Call",
                "description": "Learn to look around with the ls command",
                "commands_taught": ["ls"],
                "steps": [
                    {
                        "story": [
                            "🔔 Alarm: \"Beep beep beep! Beep beep beep!\"",
                            "",
                            "📻 Radio: \"Good Morning, this is the 9am news.\"",
                            "\"The town of Folderton has awoken to strange news. There have been",
                            "reports of missing people and damaged buildings across the town, with",
                            "more stories coming in as we speak.\"",
                            "",
                            "\"Mayor Hubert has called an emergency town meeting and we'll keep",
                            "you posted as it happens...\"",
                            "",
                            "It's time to get up sleepy head! 😴",
                            "",
                            "💡 NEW POWER: Type 'ls' and press Enter to look around."
                        ],
                        "objective": "Type 'ls' and press Enter to look around your bedroom",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["ls"],
                        "hints": [
                            "Type 'ls' and press Enter to take a look around your bedroom."
                        ],
                        "next": [2, 1]
                    }
                ]
            },
            
            # Challenge 2: Introduction to cat
            {
                "title": "Examining Objects",
                "description": "Learn to examine objects with the cat command",
                "commands_taught": ["cat"],
                "steps": [
                    {
                        "story": [
                            "Awesome, now you can see the objects around you.",
                            "There's your bed, an alarm... 🛏️ ⏰",
                            "",
                            "Euuughh...turn that alarm off! 😫",
                            "",
                            "💡 NEW POWER: To examine objects, type 'cat' and the object name."
                        ],
                        "objective": "Use 'cat alarm' to examine the alarm",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["cat alarm"],
                        "hints": [
                            "Type 'cat alarm' to investigate the alarm."
                        ],
                        "next": [2, 2]
                    },
                    {
                        "story": [
                            "Ok - it's switched off. Better get dressed... 👕",
                            "",
                            "Type 'ls wardrobe/' to look inside your wardrobe."
                        ],
                        "objective": "Look inside your wardrobe",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["ls wardrobe/", "ls wardrobe"],
                        "hints": [
                            "Type 'ls wardrobe/' to look for something to wear."
                        ],
                        "next": [3, 1]
                    }
                ]
            },
            
            # Challenge 3: More cat practice with wardrobe
            {
                "title": "Getting Dressed",
                "description": "Practice using cat to examine clothing",
                "commands_taught": ["cat"],
                "steps": [
                    {
                        "story": [
                            "Check out that t-shirt! 👕",
                            "",
                            "Examine the t-shirt with 'cat wardrobe/t-shirt' to see how it looks."
                        ],
                        "objective": "Examine the t-shirt",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["cat wardrobe/t-shirt"],
                        "hints": [
                            "Type 'cat wardrobe/t-shirt' to investigate how it looks."
                        ],
                        "next": [3, 2]
                    },
                    {
                        "story": [
                            "Looking good! Put that on and look for something else.",
                            "",
                            "Examine the skirt or the trousers.",
                            "Choose what you want to wear! 👗👖"
                        ],
                        "objective": "Examine either the skirt or trousers",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["cat wardrobe/skirt", "cat wardrobe/trousers"],
                        "hints": [
                            "Type 'cat wardrobe/trousers' or 'cat wardrobe/skirt' to dress yourself.",
                            "You need to look in your wardrobe for that item."
                        ],
                        "next": [3, 3]
                    },
                    {
                        "story": [
                            "Awesome, you're nearly dressed to quest! ✨",
                            "",
                            "Finally, check out that cap. 🧢"
                        ],
                        "objective": "Examine the cap",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["cat wardrobe/cap"],
                        "hints": [
                            "Type 'cat wardrobe/cap' to examine the cap."
                        ],
                        "next": [4, 1]
                    }
                ]
            },
            
            # Challenge 4: Exploring the shelves
            {
                "title": "Exploring Your Room",
                "description": "Discover more items in your room",
                "commands_taught": ["ls", "cat"],
                "steps": [
                    {
                        "story": [
                            "Love it! Put it on quickly. 🧢",
                            "There's loads more interesting stuff in your room.",
                            "",
                            "Let's look in your shelves using 'ls'."
                        ],
                        "objective": "Look at your shelves",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["ls shelves", "ls shelves/"],
                        "hints": [
                            "Type 'ls shelves/' to look at your books."
                        ],
                        "next": [4, 2]
                    },
                    {
                        "story": [
                            "Did you know you can use the TAB key to speed up your typing? ⚡",
                            "Try it by checking out that comic book.",
                            "",
                            "Examine it with 'cat shelves/comic-book'",
                            "Press the TAB key before you've finished typing! 📚"
                        ],
                        "objective": "Read the comic book",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["cat shelves/comic-book"],
                        "hints": [
                            "Type 'cat shelves/comic-book' to read the comic."
                        ],
                        "next": [4, 3]
                    },
                    {
                        "story": [
                            "Why is it covered in pawprints? 🐾",
                            "Hang on, can you see that? There's a note amongst your books.",
                            "",
                            "Read the note using 'cat'."
                        ],
                        "objective": "Read the mysterious note",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["cat shelves/note"],
                        "hints": [
                            "Type 'cat shelves/note' to read the note."
                        ],
                        "next": [5, 1]
                    }
                ]
            },
            
            # Challenge 5: Introduction to cd
            {
                "title": "Moving Around",
                "description": "Learn to change directories with cd",
                "commands_taught": ["cd"],
                "steps": [
                    {
                        "story": [
                            "That's weird. No time for that now though - let's find Mum. 👩",
                            "",
                            "💡 NEW POWER: 'cd' lets you move between places.",
                            "",
                            "Use the command 'cd ..' to leave your room.",
                            "The '..' means the place behind you."
                        ],
                        "objective": "Leave your room using 'cd ..'",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house",
                        "commands": ["cd ..", "cd ../", "cd ~/my-house", "cd ~/my-house/"],
                        "hints": [
                            "Type 'cd ..' to leave your room. The '..' is the room behind you.",
                            "Type 'cd ..' to leave your room."
                        ],
                        "next": [5, 2]
                    },
                    {
                        "story": [
                            "You've left my-room and are in the hall of my-house. 🏠",
                            "",
                            "Look around at the different rooms using 'ls'."
                        ],
                        "objective": "Look around the house",
                        "start_dir": "~/my-house",
                        "end_dir": "~/my-house",
                        "commands": ["ls"],
                        "hints": [
                            "Type 'ls' and press Enter."
                        ],
                        "next": [5, 3]
                    },
                    {
                        "story": [
                            "🔔 Ding. Dong. 🔔",
                            "",
                            "What was that? A bell? That's a bit odd.",
                            "You see the door to your kitchen, and hear the sound of cooking.",
                            "Sounds like someone is preparing breakfast! 🍳",
                            "",
                            "To go inside the kitchen, use 'cd kitchen'"
                        ],
                        "objective": "Go to the kitchen",
                        "start_dir": "~/my-house",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["cd kitchen", "cd kitchen/"],
                        "hints": [
                            "Type 'cd kitchen' and press Enter."
                        ],
                        "next": [6, 1]
                    }
                ]
            },
            
            # Challenge 6: Meeting Mum
            {
                "title": "Finding Mum",
                "description": "Talk to Mum in the kitchen",
                "commands_taught": ["cat"],
                "steps": [
                    {
                        "story": [
                            "Great, you're in the kitchen. 🍳",
                            "",
                            "Look around to see what's here."
                        ],
                        "objective": "Look around the kitchen",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["ls"],
                        "hints": [
                            "Type 'ls' to see what's in the kitchen."
                        ],
                        "next": [6, 2]
                    },
                    {
                        "story": [
                            "There's Mum! Talk to her to see what she says. 👩‍🍳"
                        ],
                        "objective": "Talk to Mum",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["cat Mum"],
                        "hints": [
                            "Type 'cat Mum' to talk to your mother."
                        ],
                        "next": [7, 1]
                    }
                ]
            },
            
            # Challenge 7: Going to find Dad
            {
                "title": "Looking for Dad",
                "description": "Navigate to the garden to find Dad",
                "commands_taught": ["cd"],
                "steps": [
                    {
                        "story": [
                            "👩 Mum: \"Hi sleepyhead, breakfast is nearly ready. Can you go and grab your Dad?",
                            "I think he's in the garden.\"",
                            "",
                            "Let's look for your Dad in the garden.",
                            "First we need to leave the kitchen using 'cd ..'"
                        ],
                        "objective": "Leave the kitchen",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house",
                        "commands": ["cd ..", "cd ../"],
                        "hints": [
                            "To leave the kitchen, type 'cd ..'"
                        ],
                        "next": [7, 2]
                    },
                    {
                        "story": [
                            "You are back in the main hall of your house.",
                            "",
                            "Can you see your garden? Have a look around you."
                        ],
                        "objective": "Look around for the garden",
                        "start_dir": "~/my-house",
                        "end_dir": "~/my-house",
                        "commands": ["ls"],
                        "hints": [
                            "Type 'ls' to look around you."
                        ],
                        "next": [7, 3]
                    },
                    {
                        "story": [
                            "You see doors to the garden, kitchen, my-room and parents-room.",
                            "Go into your garden. 🌻"
                        ],
                        "objective": "Go to the garden",
                        "start_dir": "~/my-house",
                        "end_dir": "~/my-house/garden",
                        "commands": ["cd garden", "cd garden/"],
                        "hints": [
                            "Type 'cd garden' to go into the garden."
                        ],
                        "next": [7, 4]
                    },
                    {
                        "story": [
                            "Use 'ls' to look in the garden for your Dad. 👨"
                        ],
                        "objective": "Look for Dad in the garden",
                        "start_dir": "~/my-house/garden",
                        "end_dir": "~/my-house/garden",
                        "commands": ["ls"],
                        "hints": [
                            "To look for your Dad, type 'ls' and press Enter."
                        ],
                        "next": [7, 5]
                    },
                    {
                        "story": [
                            "The garden looks beautiful at this time of year. 🌺",
                            "Hmmm...but you can't see him anywhere.",
                            "Maybe he's in the greenhouse. 🏠",
                            "",
                            "Go inside the greenhouse."
                        ],
                        "objective": "Go to the greenhouse",
                        "start_dir": "~/my-house/garden",
                        "end_dir": "~/my-house/garden/greenhouse",
                        "commands": ["cd greenhouse", "cd greenhouse/"],
                        "hints": [
                            "To go to the greenhouse, type 'cd greenhouse'"
                        ],
                        "next": [8, 1]
                    }
                ]
            },
            
            # Challenge 8: Finding the note
            {
                "title": "The Greenhouse Mystery",
                "description": "Discover what happened to Dad",
                "commands_taught": ["ls", "cat"],
                "steps": [
                    {
                        "story": [
                            "Look around the greenhouse for Dad. 🔍"
                        ],
                        "objective": "Search the greenhouse",
                        "start_dir": "~/my-house/garden/greenhouse",
                        "end_dir": "~/my-house/garden/greenhouse",
                        "commands": ["ls"],
                        "hints": [
                            "Type 'ls' to look around the greenhouse."
                        ],
                        "next": [8, 2]
                    },
                    {
                        "story": [
                            "Dad's not here, but there's a note! 📝",
                            "That's strange... what does it say?",
                            "",
                            "Read the note to find out what happened."
                        ],
                        "objective": "Read the note",
                        "start_dir": "~/my-house/garden/greenhouse",
                        "end_dir": "~/my-house/garden/greenhouse",
                        "commands": ["cat note"],
                        "hints": [
                            "Type 'cat note' to read what the note says."
                        ],
                        "next": [9, 1]
                    }
                ]
            },
            
            # Challenge 9: pwd command
            {
                "title": "Where Am I?",
                "description": "Learn to check your location with pwd",
                "commands_taught": ["pwd"],
                "steps": [
                    {
                        "story": [
                            "That's concerning! We need to tell Mum about this. 😟",
                            "",
                            "But first, let's learn a useful command.",
                            "Sometimes you might forget where you are.",
                            "The 'pwd' command shows your current location.",
                            "",
                            "💡 NEW POWER: 'pwd' shows where you are."
                        ],
                        "objective": "Type 'pwd' to see where you are",
                        "start_dir": "~/my-house/garden/greenhouse",
                        "end_dir": "~/my-house/garden/greenhouse",
                        "commands": ["pwd"],
                        "hints": [
                            "Type 'pwd' to print your working directory."
                        ],
                        "next": [10, 1]
                    }
                ]
            },
            
            # Challenge 10: Back to Mum - Tell her about the note
            {
                "title": "Back to Mum",
                "description": "Navigate back to tell Mum what you found",
                "commands_taught": ["cd"],
                "steps": [
                    {
                        "story": [
                            "You're in ~/my-house/garden/greenhouse! 📍",
                            "",
                            "That note was concerning! We need to tell Mum about this.",
                            "Let's go back to the kitchen step by step.",
                            "",
                            "First, go back to the garden using 'cd ..'"
                        ],
                        "objective": "Go back to the garden",
                        "start_dir": "~/my-house/garden/greenhouse",
                        "end_dir": "~/my-house/garden",
                        "commands": ["cd ..", "cd ../"],
                        "hints": [
                            "Type 'cd ..' to go back to the garden.",
                            "💡 TIP: Press the UP arrow key to replay your previous command!"
                        ],
                        "next": [10, 2]
                    },
                    {
                        "story": [
                            "You're back in the garden. 🌻",
                            "Use 'cd ..' again to go back to the house.",
                            "",
                            "💡 TIP: Press the UP arrow key to replay your previous command!"
                        ],
                        "objective": "Go back to the house",
                        "start_dir": "~/my-house/garden",
                        "end_dir": "~/my-house",
                        "commands": ["cd ..", "cd ../"],
                        "hints": [
                            "Type 'cd ..' to go back to the house."
                        ],
                        "next": [10, 3]
                    },
                    {
                        "story": [
                            "Now go back into the kitchen to see Mum. 👩‍🍳"
                        ],
                        "objective": "Go to the kitchen",
                        "start_dir": "~/my-house",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["cd kitchen", "cd kitchen/"],
                        "hints": [
                            "Type 'cd kitchen' to go back to the kitchen."
                        ],
                        "next": [11, 1]
                    }
                ]
            },
            
            # Challenge 11: Tell Mum about Dad
            {
                "title": "Breaking the News",
                "description": "Tell Mum what you discovered about Dad",
                "commands_taught": ["cat"],
                "steps": [
                    {
                        "story": [
                            "Let Mum know about Dad. 😟",
                            "Talk to her using 'cat Mum'"
                        ],
                        "objective": "Talk to Mum about Dad",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["cat Mum"],
                        "hints": [
                            "To talk to your Mum, type 'cat Mum' and press Enter."
                        ],
                        "next": [12, 1]
                    }
                ]
            },
            
            # Challenge 12: Journey to Town
            {
                "title": "The Journey to Town",
                "description": "Learn to navigate to town and explore new areas",
                "commands_taught": ["cd", "ls"],
                "steps": [
                    {
                        "story": [
                            "👩 Mum: \"You couldn't find him? That's strange, he never leaves home",
                            "without telling me first.\"",
                            "",
                            "\"Maybe he went to that town meeting with the Mayor, the one they were",
                            "talking about on the news. Why don't you go and check? I'll stay here",
                            "in case he comes back.\"",
                            "",
                            "Let's head to town! To leave the house, use 'cd' by itself.",
                            "This will take you to the main road."
                        ],
                        "objective": "Leave the house to start your journey",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~",
                        "commands": ["cd"],
                        "hints": [
                            "Type 'cd' by itself to start the journey.",
                            "Using 'cd' alone takes you to your home directory (~)."
                        ],
                        "next": [12, 2]
                    },
                    {
                        "story": [
                            "You're out of the house and on the long windy road called Tilde, or ~! 🛣️",
                            "",
                            "This is the main road that connects all the places in your world.",
                            "Look around to see where you can go next."
                        ],
                        "objective": "Look around the main road",
                        "start_dir": "~",
                        "end_dir": "~",
                        "commands": ["ls"],
                        "hints": [
                            "Type 'ls' to look around and see what's available."
                        ],
                        "next": [12, 3]
                    },
                    {
                        "story": [
                            "You can see a town in the distance! 🏘️",
                            "Let's go there using 'cd town'."
                        ],
                        "objective": "Go to the town",
                        "start_dir": "~",
                        "end_dir": "~/town",
                        "commands": ["cd town", "cd town/"],
                        "hints": [
                            "Type 'cd town' to walk into town."
                        ],
                        "next": [13, 1]
                    }
                ]
            },
            
            # Challenge 13: Exploring the Town
            {
                "title": "Welcome to Town",
                "description": "Explore the town and meet the townspeople",
                "commands_taught": ["ls", "cat"],
                "steps": [
                    {
                        "story": [
                            "Welcome to the town of Folderton! 🏘️",
                            "",
                            "This is where the strange events from the radio news are happening.",
                            "Have a look around to see what's going on!"
                        ],
                        "objective": "Look around the town",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["ls"],
                        "hints": [
                            "Use 'ls' to look around and see who's in town."
                        ],
                        "next": [13, 2]
                    },
                    {
                        "story": [
                            "Wow, there's so many people here! 👥",
                            "You can see the Mayor, and several townspeople.",
                            "",
                            "Find the Mayor and listen to what he has to say.",
                            "Maybe he knows something about Dad!"
                        ],
                        "objective": "Talk to the Mayor",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["cat Mayor"],
                        "hints": [
                            "Type 'cat Mayor' to listen to the Mayor."
                        ],
                        "next": [13, 3]
                    },
                    {
                        "story": [
                            "🏛️ Mayor: \"Calm down please! We have our best people looking into",
                            "the disappearances, and we're hoping to have an explanation soon.\"",
                            "",
                            "Disappearances? That sounds serious! 😟",
                            "Something strange is definitely happening here.",
                            "",
                            "Better check on the other people to see if they're okay.",
                            "Talk to some of the townspeople to learn more."
                        ],
                        "objective": "Talk to the townspeople (grumpy-man, young-girl, or little-boy)",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["cat grumpy-man", "cat young-girl", "cat little-boy"],
                        "hints": [
                            "Try 'cat grumpy-man', 'cat young-girl', or 'cat little-boy'",
                            "Talk to any of the townspeople to learn what's happening."
                        ],
                        "next": [14, 1]
                    }
                ]
            },
            
            # Challenge 14: The Mystery Deepens
            {
                "title": "Strange Happenings",
                "description": "Discover the mystery of the disappearing people",
                "commands_taught": ["cat", "ls"],
                "steps": [
                    {
                        "story": [
                            "The townspeople are clearly worried about something! 😰",
                            "",
                            "Each person you talk to reveals more about the mystery:",
                            "• The grumpy man mentions strange bells and his legs feeling odd",
                            "• The young girl is looking for her missing friend Amy", 
                            "• The little boy has lost his dog Pongo",
                            "",
                            "This is definitely connected to the news report you heard this morning!",
                            "Continue talking to people to gather more information.",
                            "",
                            "Talk to at least 2 more townspeople to learn what's happening."
                        ],
                        "objective": "Talk to more townspeople (any 2 of the 3)",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["cat grumpy-man", "cat young-girl", "cat little-boy"],
                        "hints": [
                            "Use 'cat' with any of the townspeople names",
                            "Try talking to grumpy-man, young-girl, and little-boy",
                            "You need to talk to at least 2 people total"
                        ],
                        "next": [15, 1]
                    }
                ]
            },
            
            # Challenge 15: Mastery Test - Navigation Skills
            {
                "title": "Navigation Mastery",
                "description": "Test your navigation skills by exploring",
                "commands_taught": ["cd", "ls", "pwd", "cat"],
                "steps": [
                    {
                        "story": [
                            "🎉 Excellent detective work! You've learned a lot about the mystery.",
                            "",
                            "You now know how to:",
                            "• Navigate between locations with 'cd'",
                            "• Explore areas with 'ls'", 
                            "• Talk to characters with 'cat'",
                            "• Check your location with 'pwd'",
                            "",
                            "Let's test your skills! Navigate back home and check on things there.",
                            "Use 'pwd' to see where you are, then go back to your house."
                        ],
                        "objective": "Check where you are, then go back to your house",
                        "start_dir": "~/town",
                        "end_dir": "~/my-house",
                        "commands": ["pwd", "cd ~/my-house", "cd ..", "cd ../my-house"],
                        "hints": [
                            "First use 'pwd' to see where you are",
                            "Then use 'cd ~/my-house' to go home directly",
                            "Or use 'cd ..' then 'cd my-house' to go step by step"
                        ],
                        "next": [16, 1]
                    }
                ]
            },
            
            # Challenge 16: The Bell Rings - First Disappearance
            {
                "title": "The Bell Rings",
                "description": "Witness the mysterious disappearances begin",
                "commands_taught": ["ls"],
                "steps": [
                    {
                        "story": [
                            "🏠 You're back at your house, but something feels different...",
                            "",
                            "Let's go back to town to check on everyone.",
                            "Use 'cd town' to return to town."
                        ],
                        "objective": "Go back to town",
                        "start_dir": "~/my-house",
                        "end_dir": "~/town",
                        "commands": ["cd town", "cd ~/town"],
                        "hints": [
                            "Use 'cd town' to go back to town"
                        ],
                        "next": [16, 2]
                    },
                    {
                        "story": [
                            "🔔 Ding. Dong.",
                            "",
                            "It sounds like the bell you heard before.",
                            "",
                            "Use 'ls' to look around again."
                        ],
                        "objective": "Look around to see what changed",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["ls"],
                        "hints": [
                            "Use 'ls' to look around."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/grumpy-man"}
                        ],
                        "next": [16, 3]
                    },
                    {
                        "story": [
                            "👦 Little-boy: \"Oh no! That grumpy-man with the funny legs has gone!\"",
                            "\"Did you hear the bell just before he vanished??\"",
                            "",
                            "👧 Young-girl: \"I'm scared...\"",
                            "",
                            "🔔 Ding. Dong.",
                            "",
                            "👧 Young-girl: \"Oh! I heard it go again!\"",
                            "",
                            "Take a look around you to check."
                        ],
                        "objective": "Look around to see what else changed",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["ls"],
                        "hints": [
                            "Use 'ls' to look around."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/little-boy"}
                        ],
                        "next": [17, 1]
                    }
                ]
            },
            
            # Challenge 17: More Disappearances
            {
                "title": "The Mystery Deepens",
                "description": "Watch as more people disappear",
                "commands_taught": ["ls", "cat"],
                "steps": [
                    {
                        "story": [
                            "👧 Young-girl: \"Wait, there was a little-boy here...right?\"",
                            "\"Every time that bell goes, someone disappears!\"",
                            "",
                            "👨‍💼 Mayor: \"Maybe they just decided to go home...?\"",
                            "",
                            "🔔 Ding. Dong.",
                            "",
                            "Look around."
                        ],
                        "objective": "Look around to see the next disappearance",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["ls"],
                        "hints": [
                            "Use 'ls' to look around."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/young-girl"}
                        ],
                        "next": [17, 2]
                    },
                    {
                        "story": [
                            "You are alone with the Mayor.",
                            "",
                            "Listen to what the Mayor has to say."
                        ],
                        "objective": "Talk to the Mayor",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["cat Mayor"],
                        "hints": [
                            "Use 'cat Mayor' to talk to the Mayor."
                        ],
                        "next": [17, 3]
                    },
                    {
                        "story": [
                            "👨‍💼 Mayor: \"Everyone...has disappeared??\"",
                            "\"....I should head home now...\"",
                            "",
                            "🔔 Ding. Dong.",
                            "",
                            "Look around one more time..."
                        ],
                        "objective": "Look around to see the final disappearance",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["ls"],
                        "hints": [
                            "Use 'ls' to look around."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/Mayor"},
                            {"action": "add", "path": "~/town/note", "type": "file", "content": "note_town"}
                        ],
                        "next": [18, 1]
                    }
                ]
            },
            
            # Challenge 18: The First Note
            {
                "title": "A Mysterious Note",
                "description": "Discover the first clue",
                "commands_taught": ["cat"],
                "steps": [
                    {
                        "story": [
                            "Everyone has gone.",
                            "Wait - there's a note on the floor.",
                            "",
                            "Use 'cat' to read the note."
                        ],
                        "objective": "Read the mysterious note",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["cat note"],
                        "hints": [
                            "Use 'cat note' to read the note."
                        ],
                        "next": [19, 1]
                    }
                ]
            },
            
            # Challenge 19: Rush Home
            {
                "title": "Racing Home",
                "description": "Rush home to check on Mum",
                "commands_taught": ["cd"],
                "steps": [
                    {
                        "story": [
                            "📝 The note says: \"There's no time to lose. Run home.\"",
                            "",
                            "Oh no! Check your Mum is alright.",
                            "",
                            "Type 'cd ..' to leave town."
                        ],
                        "objective": "Leave town to head home",
                        "start_dir": "~/town",
                        "end_dir": "~",
                        "commands": ["cd ..", "cd ../", "cd"],
                        "hints": [
                            "Use 'cd ..' to start heading back home."
                        ],
                        "next": [19, 2]
                    },
                    {
                        "story": [
                            "🔔 Ding. Dong.",
                            "",
                            "Type 'cd my-house/kitchen' to go straight to the kitchen.",
                            "",
                            "💡 Press TAB to speed up your typing!"
                        ],
                        "objective": "Go directly to the kitchen",
                        "start_dir": "~",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["cd my-house/kitchen", "cd my-house/kitchen/"],
                        "hints": [
                            "Use 'cd my-house/kitchen' to go to the kitchen."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/my-house/kitchen/Mum"},
                            {"action": "add", "path": "~/my-house/kitchen/note", "type": "file", "content": "note_kitchen"},
                            {"action": "remove", "path": "~/town/note"}
                        ],
                        "next": [19, 3]
                    },
                    {
                        "story": [
                            "Take a look around to make sure everything is OK."
                        ],
                        "objective": "Look around the kitchen",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["ls"],
                        "hints": [
                            "Use 'ls' to see that everything is where it should be."
                        ],
                        "next": [19, 4]
                    },
                    {
                        "story": [
                            "Oh no - Mum has vanished too!",
                            "Wait, there's another note.",
                            "",
                            "Use 'cat' to read the note."
                        ],
                        "objective": "Read the second note",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["cat note"],
                        "hints": [
                            "Use 'cat note' to read the note."
                        ],
                        "next": [20, 1]
                    }
                ]
            },
            
            # Challenge 20: Exploring the Kitchen
            {
                "title": "Searching for Clues",
                "description": "Examine objects in the kitchen for clues",
                "commands_taught": ["cat"],
                "steps": [
                    {
                        "story": [
                            "📝 The note says: \"Prepare yourself.\"",
                            "",
                            "You're in your house. You appear to be alone.",
                            "Use 'cat' to examine some of the objects around you.",
                            "",
                            "Look at at least 2 different food items to search for clues."
                        ],
                        "objective": "Examine 2 different food items in the kitchen",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["cat banana", "cat cake", "cat croissant", "cat grapes", "cat milk", "cat newspaper", "cat pie", "cat sandwich"],
                        "hints": [
                            "Use 'cat' to look at two of the food items around you.",
                            "Try examining items like banana, cake, grapes, milk, pie, or sandwich"
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/my-house/kitchen/note"}
                        ],
                        "next": [21, 1]
                    }
                ]
            },
            
            # Challenge 21: The Hidden Shelter Discovery
            {
                "title": "The Hidden Shelter",
                "description": "Discover the secret shelter using ls -a",
                "commands_taught": ["ls -a", "cd"],
                "steps": [
                    {
                        "story": [
                            "There doesn't seem to be anything here but loads of food.",
                            "See if you can find something back in town.",
                            "",
                            "First, use 'cd ..' to leave the kitchen."
                        ],
                        "objective": "Leave the kitchen",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house",
                        "commands": ["cd ..", "cd ../"],
                        "hints": [
                            "Use 'cd ..' to leave the kitchen."
                        ],
                        "next": [21, 2]
                    },
                    {
                        "story": [
                            "Now navigate back to town to continue searching.",
                            "Use 'cd ../town' to go to town."
                        ],
                        "objective": "Go back to town",
                        "start_dir": "~/my-house",
                        "end_dir": "~/town",
                        "commands": ["cd ../town", "cd ~/town", "cd ..", "cd town"],
                        "hints": [
                            "Use 'cd ../town' or 'cd ~/town' to go to town."
                        ],
                        "next": [21, 3]
                    },
                    {
                        "story": [
                            "Use 'ls' to look around."
                        ],
                        "objective": "Look around the empty town",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["ls"],
                        "hints": [
                            "Use 'ls' to have a look around the town."
                        ],
                        "next": [21, 4]
                    },
                    {
                        "story": [
                            "The place appears to be deserted.",
                            "However, you think you hear whispers.",
                            "",
                            "🗣️ ?: \".....if they use ls -a, they'll see us...\"",
                            "🗣️ ?: \"..Shhh! ...might hear....\""
                        ],
                        "objective": "Use the mysterious command you overheard",
                        "start_dir": "~/town",
                        "end_dir": "~/town",
                        "commands": ["ls -a"],
                        "hints": [
                            "You heard whispers referring to 'ls -a', try using it!"
                        ],
                        "next": [21, 5]
                    },
                    {
                        "story": [
                            "You see a .hidden-shelter that you didn't notice before!",
                            "",
                            "💡 Something that starts with . is normally hidden from view.",
                            "",
                            "It sounds like the whispers are coming from there. Try going in."
                        ],
                        "objective": "Enter the hidden shelter",
                        "start_dir": "~/town",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["cd .hidden-shelter", "cd .hidden-shelter/"],
                        "hints": [
                            "Try going inside the .hidden-shelter using cd",
                            "Use the command 'cd .hidden-shelter' to go inside."
                        ],
                        "next": [22, 1]
                    }
                ]
            },
            
            # Challenge 22: Meeting the Survivors
            {
                "title": "The Survivors",
                "description": "Meet the people who escaped the disappearances",
                "commands_taught": ["ls", "cat"],
                "steps": [
                    {
                        "story": [
                            "Is anyone there? Have a look around."
                        ],
                        "objective": "Look around the hidden shelter",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["ls", "ls -a"],
                        "hints": [
                            "Use 'ls' to have a look around you."
                        ],
                        "next": [22, 2]
                    },
                    {
                        "story": [
                            "🎉 Amazing! You found the survivors!",
                            "",
                            "There are people here: Eleanor, Edward, Edith, and even a dog!",
                            "Talk to them to learn what happened.",
                            "",
                            "Use 'cat' to talk to at least 2 of the survivors."
                        ],
                        "objective": "Talk to at least 2 survivors",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["cat Eleanor", "cat Edward", "cat Edith", "cat dog"],
                        "hints": [
                            "Use 'cat' with the names Eleanor, Edward, or Edith",
                            "Talk to at least 2 people to learn their stories"
                        ],
                        "next": [23, 1]
                    }
                ]
            },
            
            # Challenge 23: Learning the mv Command
            {
                "title": "Learning to Move Things",
                "description": "Learn the mv command to move objects around",
                "commands_taught": ["mv"],
                "steps": [
                    {
                        "story": [
                            "👨 Edward: \"You found us! I told you to keep your voice down, Edith.\"",
                            "",
                            "👩 Edith: \"Edward, I don't think they mean any harm. Maybe they could help us?\"",
                            "",
                            "👧 Eleanor: \"My mummy is scared the bell will find us if we go outside.\"",
                            "",
                            "🐕 Dog: \"Woof woof!\"",
                            "",
                            "Edward looks like he has something he wants to say to you.",
                            "",
                            "👨 Edward: \"Hey! Can you help me?\"",
                            "\"I've been trying to move this apple into the basket.\"",
                            "\"I was told the command 'mv apple basket/' would make it happen,\"",
                            "\"but I can't seem to make it work. Do you have the power to make it happen?\"",
                            "",
                            "💡 NEW POWER: To move objects, type 'mv' and the object name."
                        ],
                        "objective": "Move the apple into the basket",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["mv apple basket", "mv apple basket/"],
                        "hints": [
                            "Use the command 'mv apple basket/' to move the apple into the basket."
                        ],
                        "next": [23, 2]
                    },
                    {
                        "story": [
                            "Check you've managed to move the apple. Look around in this directory."
                        ],
                        "objective": "Look around to see the apple is gone",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["ls", "ls -a"],
                        "hints": [
                            "Use 'ls' to look around."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/.hidden-shelter/apple"},
                            {"action": "add", "path": "~/town/.hidden-shelter/basket/apple", "type": "file", "content": "apple"}
                        ],
                        "next": [23, 3]
                    },
                    {
                        "story": [
                            "✅ Nice work! The apple isn't in this directory anymore.",
                            "",
                            "Now check the apple is in the basket using 'ls'."
                        ],
                        "objective": "Check the apple is in the basket",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["ls basket", "ls basket/", "ls -a basket", "ls -a basket/"],
                        "hints": [
                            "Use the command 'ls basket/' to look in the basket."
                        ],
                        "next": [23, 4]
                    },
                    {
                        "story": [
                            "✅ Excellent, you moved the apple into the basket!",
                            "",
                            "👨 Edward: \"Wow, you did it!\"",
                            "\"Can you also move the apple from the basket back to here?\"",
                            "",
                            "Move the apple back to your current location using '.' (dot)."
                        ],
                        "objective": "Move the apple back from the basket",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["mv basket/apple .", "mv basket/apple ./"],
                        "hints": [
                            "Use the command 'mv basket/apple ./' to move the apple from the basket to your current position (./)"
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/.hidden-shelter/basket/apple"},
                            {"action": "add", "path": "~/town/.hidden-shelter/apple", "type": "file", "content": "apple"}
                        ],
                        "next": [24, 1]
                    }
                ]
            },
            
            # Challenge 24: Rescuing Eleanor and the Dog
            {
                "title": "The Great Rescue",
                "description": "Use mv to rescue Eleanor and the dog who wandered outside",
                "commands_taught": ["mv", "ls"],
                "steps": [
                    {
                        "story": [
                            "👩 Edith: \"You should stop playing with that, that's the last of our food.\"",
                            "\"Ah! The dog ran outside!\"",
                            "",
                            "👧 Eleanor: \"Doggy!\"",
                            "",
                            "👩 Edith: \"No, honey! Don't go outside!\"",
                            "",
                            "Eleanor follows her dog and leaves the .hidden-shelter.",
                            "Look around to check this."
                        ],
                        "objective": "Look around to see Eleanor and dog are gone",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["ls", "ls -a"],
                        "hints": [
                            "Look around using 'ls' to check if Eleanor is here."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/.hidden-shelter/Eleanor"},
                            {"action": "remove", "path": "~/town/.hidden-shelter/dog"},
                            {"action": "add", "path": "~/town/Eleanor", "type": "file", "content": "Eleanor"},
                            {"action": "add", "path": "~/town/dog", "type": "file", "content": "dog"}
                        ],
                        "next": [24, 2]
                    },
                    {
                        "story": [
                            "👩 Edith: \"No! Honey, come back!!!\"",
                            "\"You, please, save my little girl!\"",
                            "",
                            "First, look outside for Eleanor with 'ls ../'."
                        ],
                        "objective": "Look outside the shelter for Eleanor",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["ls ..", "ls ../", "ls ~/town", "ls ~/town/"],
                        "hints": [
                            "Look in the town directory by using either 'ls ../' or 'ls ~/town/'"
                        ],
                        "next": [24, 3]
                    },
                    {
                        "story": [
                            "Now move Eleanor from the town outside (..) to your current position (.)."
                        ],
                        "objective": "Rescue Eleanor by moving her back to safety",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["mv ../Eleanor .", "mv ../Eleanor ./", "mv ~/town/Eleanor ~/town/.hidden-shelter", "mv ~/town/Eleanor ~/town/.hidden-shelter/", "mv ~/town/Eleanor .", "mv ~/town/Eleanor ./"],
                        "hints": [
                            "Quick! Use 'mv ../Eleanor ./' to move the little girl back to safety."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/Eleanor"},
                            {"action": "add", "path": "~/town/.hidden-shelter/Eleanor", "type": "file", "content": "Eleanor"}
                        ],
                        "next": [24, 4]
                    },
                    {
                        "story": [
                            "👩 Edith: \"Thank you for saving her!\"",
                            "",
                            "👧 Eleanor: \"Doggy!\"",
                            "",
                            "👩 Edith: \"Can you save her dog too? I'm worried something will happen to it if it stays outside.\""
                        ],
                        "objective": "Rescue the dog too",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["mv ../dog .", "mv ../dog ./", "mv ~/town/dog ~/town/.hidden-shelter", "mv ~/town/dog ~/town/.hidden-shelter/", "mv ~/town/dog .", "mv ~/town/dog ./"],
                        "hints": [
                            "Use the command 'mv ../dog ./' to rescue the dog."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/dog"},
                            {"action": "add", "path": "~/town/.hidden-shelter/dog", "type": "file", "content": "dog"}
                        ],
                        "next": [25, 1]
                    }
                ]
            },
            
            # Challenge 25: Gathering Food for the Family
            {
                "title": "Gathering Food",
                "description": "Help gather food for the hungry family",
                "commands_taught": ["mv", "cd"],
                "steps": [
                    {
                        "story": [
                            "👧 Eleanor: \"Yay, Doggie!\"",
                            "",
                            "🐕 Dog: \"Ruff!\"",
                            "",
                            "👩 Edith: \"Thank you so much for getting them both back.",
                            "I was wrong about you. You're a hero!\"",
                            "",
                            "👨 Edward: \"Thank you so much for saving my little girl!",
                            "I have another favour to ask...\"",
                            "\"We haven't got any food. Could you gather some for us?",
                            "We didn't have time to grab any before we went into hiding.\"",
                            "\"Do you remember seeing any food in your travels?\"",
                            "",
                            "...ah! You have all that food in your kitchen!",
                            "We could give that to this family.",
                            "",
                            "Start by moving the basket to ~ (home).",
                            "Use the command 'mv basket ~/'."
                        ],
                        "objective": "Move the basket to the home directory",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["mv basket ~", "mv basket/ ~", "mv basket ~/", "mv basket/ ~/", "mv basket ../..", "mv basket/ ../..", "mv basket ../../", "mv basket/ ../../"],
                        "hints": [
                            "Use the command 'mv basket ~/' to move the basket to the windy road ~"
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/town/.hidden-shelter/basket"},
                            {"action": "add", "path": "~/basket", "type": "directory"}
                        ],
                        "next": [25, 2]
                    },
                    {
                        "story": [
                            "Now follow the basket. Use 'cd' by itself to go to the windy road ~."
                        ],
                        "objective": "Go to the home directory",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~",
                        "commands": ["cd", "cd ~", "cd ~/"],
                        "hints": [
                            "Use the command 'cd' by itself to move yourself to the road ~"
                        ],
                        "next": [25, 3]
                    },
                    {
                        "story": [
                            "You are now back on the long windy road. Look around with 'ls' to check that you have your basket with you."
                        ],
                        "objective": "Check that the basket is here",
                        "start_dir": "~",
                        "end_dir": "~",
                        "commands": ["ls"],
                        "hints": [
                            "Use 'ls' by itself to look around."
                        ],
                        "next": [25, 4]
                    },
                    {
                        "story": [
                            "You have your basket safely alongside you, and you see my-house close by.",
                            "Move the basket to my-house/kitchen.",
                            "Don't forget to use the TAB key to autocomplete your commands."
                        ],
                        "objective": "Move the basket to the kitchen",
                        "start_dir": "~",
                        "end_dir": "~",
                        "commands": ["mv basket my-house/kitchen", "mv basket/ my-house/kitchen", "mv basket my-house/kitchen/", "mv basket/ my-house/kitchen/", "mv basket ~/my-house/kitchen", "mv basket/ ~/my-house/kitchen", "mv basket ~/my-house/kitchen/", "mv basket/ ~/my-house/kitchen/"],
                        "hints": [
                            "Use 'mv basket my-house/kitchen/' to move the basket to your kitchen."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/basket"},
                            {"action": "add", "path": "~/my-house/kitchen/basket", "type": "directory"}
                        ],
                        "next": [26, 1]
                    }
                ]
            },
            
            # Challenge 26: Filling the Basket with Food
            {
                "title": "Filling the Basket",
                "description": "Fill the basket with food for the family",
                "commands_taught": ["mv", "cd"],
                "steps": [
                    {
                        "story": [
                            "Now go into my-house/kitchen using 'cd'."
                        ],
                        "objective": "Go to the kitchen",
                        "start_dir": "~",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["cd my-house/kitchen", "cd my-house/kitchen/", "cd ~/my-house/kitchen", "cd ~/my-house/kitchen/"],
                        "hints": [
                            "Use 'cd my-house/kitchen' to go to your kitchen."
                        ],
                        "next": [26, 2]
                    },
                    {
                        "story": [
                            "Let's look around to see what food is available in the kitchen."
                        ],
                        "objective": "Look around the kitchen",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["ls", "ls -a"],
                        "hints": [
                            "Use 'ls' to have a look around the kitchen."
                        ],
                        "next": [26, 3]
                    },
                    {
                        "story": [
                            "Move three pieces of food into your basket.",
                            "",
                            "You can move multiple items using 'mv item1 item2 item3 basket/'",
                            "For example: mv banana cake milk basket/"
                        ],
                        "objective": "Move 3 food items into the basket",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["mv banana basket", "mv cake basket", "mv croissant basket", "mv pie basket", "mv grapes basket", "mv milk basket", "mv sandwich basket"],
                        "hints": [
                            "Move food items like banana, cake, grapes, milk, pie, or sandwich into the basket",
                            "Use 'mv banana basket/' to move the banana",
                            "You need to move at least 3 food items"
                        ],
                        "next": [27, 1]
                    }
                ]
            },
            
            # Challenge 27: Delivering the Food
            {
                "title": "Delivering the Food",
                "description": "Deliver the food-filled basket to the family",
                "commands_taught": ["mv", "cd"],
                "steps": [
                    {
                        "story": [
                            "Now we want to head back to the .hidden-shelter with the basket.",
                            "Move the basket back to ~."
                        ],
                        "objective": "Move the basket back to home",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~/my-house/kitchen",
                        "commands": ["mv basket ~", "mv basket/ ~", "mv basket ~/", "mv basket/ ~/"],
                        "hints": [
                            "Use the command 'mv basket ~/' to move the basket to the windy road ~"
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/my-house/kitchen/basket"},
                            {"action": "add", "path": "~/basket", "type": "directory"}
                        ],
                        "next": [27, 2]
                    },
                    {
                        "story": [
                            "Follow the basket by using 'cd'."
                        ],
                        "objective": "Go back to home directory",
                        "start_dir": "~/my-house/kitchen",
                        "end_dir": "~",
                        "commands": ["cd", "cd ~", "cd ~/"],
                        "hints": [
                            "Use the command 'cd' by itself to move yourself to the road ~"
                        ],
                        "next": [27, 3]
                    },
                    {
                        "story": [
                            "Now get the food-filled basket to the family.",
                            "Move the basket to town/.hidden-shelter."
                        ],
                        "objective": "Move the basket to the hidden shelter",
                        "start_dir": "~",
                        "end_dir": "~",
                        "commands": ["mv basket town/.hidden-shelter", "mv basket/ town/.hidden-shelter", "mv basket town/.hidden-shelter/", "mv basket/ town/.hidden-shelter/", "mv basket ~/town/.hidden-shelter", "mv basket/ ~/town/.hidden-shelter", "mv basket ~/town/.hidden-shelter/", "mv basket/ ~/town/.hidden-shelter/"],
                        "hints": [
                            "Use 'mv basket town/.hidden-shelter/' to move the basket to the family."
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/basket"},
                            {"action": "add", "path": "~/town/.hidden-shelter/basket", "type": "directory"}
                        ],
                        "next": [27, 4]
                    },
                    {
                        "story": [
                            "Enter the town/.hidden-shelter using 'cd'."
                        ],
                        "objective": "Go back to the hidden shelter",
                        "start_dir": "~",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["cd town/.hidden-shelter", "cd town/.hidden-shelter/", "cd ~/town/.hidden-shelter", "cd ~/town/.hidden-shelter/"],
                        "hints": [
                            "Use 'cd town/.hidden-shelter' to be reunited with the family."
                        ],
                        "next": [28, 1]
                    }
                ]
            },
            
            # Challenge 28: Happy Family
            {
                "title": "A Happy Family",
                "description": "Check on the family with their new food supply",
                "commands_taught": ["cat"],
                "steps": [
                    {
                        "story": [
                            "Check on everyone with 'cat' to see if they're happy with the food."
                        ],
                        "objective": "Talk to all the family members",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["cat Edith", "cat Eleanor", "cat Edward", "cat dog"],
                        "hints": [
                            "Check on everyone using 'cat'",
                            "Talk to Edith, Eleanor, Edward, and the dog"
                        ],
                        "next": [29, 1]
                    }
                ]
            },
            
            # Challenge 29: Finding More Hidden Items
            {
                "title": "More Hidden Treasures",
                "description": "Discover more hidden items using ls -a",
                "commands_taught": ["ls -a"],
                "steps": [
                    {
                        "story": [
                            "👩 Edith: \"You saved my little girl and my dog, and now you've saved us from starvation...how can I thank you?\"",
                            "",
                            "👧 Eleanor: \"Yummy! See, I told you doggy, someone would help us.\"",
                            "",
                            "👨 Edward: \"Thank you! I knew you would come through for us. You really are a hero!\"",
                            "",
                            "🐕 Dog: \"Woof!\" (The dog seems very excited.)",
                            "",
                            "You get the nagging feeling that you're missing something.",
                            "What was the command that helped you find the hidden shelter?",
                            "",
                            "Use it to have a closer look around."
                        ],
                        "objective": "Look more closely around the shelter",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["ls -a"],
                        "hints": [
                            "Use 'ls -a' to look more closely around you."
                        ],
                        "next": [29, 2]
                    },
                    {
                        "story": [
                            "What's that? There's a .tiny-chest in the corner of the shelter.",
                            "Have a look inside the .tiny-chest."
                        ],
                        "objective": "Look inside the tiny chest",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["ls .tiny-chest", "ls .tiny-chest/", "ls -a .tiny-chest", "ls -a .tiny-chest/"],
                        "hints": [
                            "Use 'ls .tiny-chest' to look inside"
                        ],
                        "next": [29, 3]
                    },
                    {
                        "story": [
                            "You see a special looking scroll with a stamp that says MV.",
                            "Read what it says."
                        ],
                        "objective": "Read the MV scroll",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/town/.hidden-shelter",
                        "commands": ["cat .tiny-chest/MV"],
                        "hints": [
                            "Use 'cat .tiny-chest/MV' to read the MV parchment"
                        ],
                        "next": [30, 1]
                    }
                ]
            },
            
            # Challenge 30: Discovering the Hidden Chest
            {
                "title": "The Hidden Chest",
                "description": "Discover the hidden chest in your room",
                "commands_taught": ["cd", "ls -a"],
                "steps": [
                    {
                        "story": [
                            "👨 Edward: \"Hey, that's our .tiny-chest. We use it to keep things safe.\"",
                            "\"That MV command is how I found out about moving objects with 'mv'.\"",
                            "\"It's probably more useful to you, please take it as a thank you for saving us.\"",
                            "",
                            "Maybe you should go back to my-house to look for more hidden items.",
                            "To quickly go back home, use 'cd ~/my-house'."
                        ],
                        "objective": "Go back to your house",
                        "start_dir": "~/town/.hidden-shelter",
                        "end_dir": "~/my-house",
                        "commands": ["cd ~/my-house/", "cd ~/my-house"],
                        "hints": [
                            "No shortcuts! Use 'cd ~/my-house' to get back to your house in one step."
                        ],
                        "next": [30, 2]
                    },
                    {
                        "story": [
                            "Let's see if we can find anything hidden around here!",
                            "Where do you think any hidden things could be?",
                            "",
                            "Try looking closely in my-room first."
                        ],
                        "objective": "Look for hidden files in your room",
                        "start_dir": "~/my-house",
                        "end_dir": "~/my-house",
                        "commands": ["ls -a my-room", "ls -a my-room/"],
                        "hints": [
                            "Stuck? Have a look in my-room.",
                            "Use 'ls -a my-room' to look for hidden files in my-room."
                        ],
                        "next": [30, 3]
                    },
                    {
                        "story": [
                            "There is an old antique .chest hidden under your bed, which you don't remember seeing before.",
                            "",
                            "You walk into my-room to have a closer look.",
                            "",
                            "Peer inside the .chest and see what it contains."
                        ],
                        "objective": "Go to your room and look inside the chest",
                        "start_dir": "~/my-house",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["cd my-room", "cd my-room/"],
                        "hints": [
                            "Use 'cd my-room' to go into your room first"
                        ],
                        "next": [31, 1]
                    }
                ]
            },
            
            # Challenge 31: Exploring the Chest and Finding Parents' Room
            {
                "title": "Ancient Scrolls",
                "description": "Explore the hidden chest and discover your parents' secrets",
                "commands_taught": ["ls", "cat", "cd"],
                "steps": [
                    {
                        "story": [
                            "Look inside the .chest to see what it contains."
                        ],
                        "objective": "Look inside the hidden chest",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["ls .chest", "ls .chest/", "ls -a .chest", "ls -a .chest/"],
                        "hints": [
                            "Use 'ls .chest' to look inside the .chest"
                        ],
                        "next": [31, 2]
                    },
                    {
                        "story": [
                            "There are some scrolls, similar to what you found in the .hidden-shelter.",
                            "They could contain more powerful commands.",
                            "",
                            "Use 'cat' to read one of the scrolls."
                        ],
                        "objective": "Read one of the command scrolls",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["cat .chest/LS", "cat .chest/CAT", "cat .chest/CD"],
                        "hints": [
                            "Use 'cat .chest/LS' to read the LS scroll."
                        ],
                        "next": [31, 3]
                    },
                    {
                        "story": [
                            "I wonder if there's anything else hidden in this .chest?",
                            "Have a closer look for some more items."
                        ],
                        "objective": "Look for hidden items in the chest",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["ls -a .chest", "ls -a .chest/"],
                        "hints": [
                            "Use 'ls -a .chest' to see if there are any hidden items in the chest."
                        ],
                        "next": [31, 4]
                    },
                    {
                        "story": [
                            "You suddenly notice a tiny stained .note, scrumpled in the corner of the .chest.",
                            "What does it say?"
                        ],
                        "objective": "Read the hidden note",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["cat .chest/.note"],
                        "hints": [
                            "Use 'cat .chest/.note' to read the .note."
                        ],
                        "next": [31, 5]
                    },
                    {
                        "story": [
                            "You're in your room, standing in front of the .chest containing all the commands you've learned so far.",
                            "",
                            "Maybe something else is hidden in the house?",
                            "",
                            "Look in the hallway behind you. Remember, behind you is '..'."
                        ],
                        "objective": "Look in the hallway",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/my-room",
                        "commands": ["ls ..", "ls ../"],
                        "hints": [
                            "Look behind you with 'ls ../'"
                        ],
                        "next": [31, 6]
                    },
                    {
                        "story": [
                            "You see doors to your garden, kitchen, my-room and parents-room.",
                            "We haven't checked out your parents' room properly yet.",
                            "",
                            "Go into your parents-room."
                        ],
                        "objective": "Go to your parents' room",
                        "start_dir": "~/my-house/my-room",
                        "end_dir": "~/my-house/parents-room",
                        "commands": ["cd ../parents-room", "cd ~/my-house/parents-room"],
                        "hints": [
                            "Use 'cd ../parents-room' to go to your parents' room"
                        ],
                        "next": [32, 1]
                    }
                ]
            },
            
            # Challenge 32: The Safe and Echo Command
            {
                "title": "The Secret Safe",
                "description": "Discover the secret safe and learn the echo command",
                "commands_taught": ["ls -a", "cat", "echo"],
                "steps": [
                    {
                        "story": [
                            "Look around closely."
                        ],
                        "objective": "Look for hidden items in parents' room",
                        "start_dir": "~/my-house/parents-room",
                        "end_dir": "~/my-house/parents-room",
                        "commands": ["ls -a", "ls -a .", "ls -a ./"],
                        "hints": [
                            "Use the command 'ls -a' to look around closely."
                        ],
                        "next": [32, 2]
                    },
                    {
                        "story": [
                            "There's a .safe!",
                            "",
                            "Maybe there's something useful in here. Look inside the .safe."
                        ],
                        "objective": "Look inside the safe",
                        "start_dir": "~/my-house/parents-room",
                        "end_dir": "~/my-house/parents-room",
                        "commands": ["ls .safe", "ls .safe/", "ls -a .safe", "ls -a .safe/"],
                        "hints": [
                            "Look in the .safe using ls.",
                            "Use 'ls .safe' to look into the .safe."
                        ],
                        "next": [32, 3]
                    },
                    {
                        "story": [
                            "So you found your Mum's diary?",
                            "You probably shouldn't read it...",
                            "",
                            "What else is here? Let's examine that map."
                        ],
                        "objective": "Read the map",
                        "start_dir": "~/my-house/parents-room",
                        "end_dir": "~/my-house/parents-room",
                        "commands": ["cat .safe/map"],
                        "hints": [
                            "Use 'cat' to read the map.",
                            "Use 'cat .safe/map' to read the map."
                        ],
                        "next": [32, 4]
                    },
                    {
                        "story": [
                            "So there's a farm around here?",
                            "Apparently it's not far from our house, just off the windy road...",
                            "",
                            "What is this ECHO note? Examine the ECHO note."
                        ],
                        "objective": "Read the ECHO scroll",
                        "start_dir": "~/my-house/parents-room",
                        "end_dir": "~/my-house/parents-room",
                        "commands": ["cat .safe/ECHO"],
                        "hints": [
                            "Use the 'cat' command to read the ECHO note.",
                            "Use 'cat .safe/ECHO' to read the note."
                        ],
                        "next": [32, 5]
                    },
                    {
                        "story": [
                            "So the note says \"echo hello - will make you say hello\"",
                            "Let's test this out.",
                            "",
                            "💡 NEW POWER: 'echo' followed by words lets you speak"
                        ],
                        "objective": "Test the echo command",
                        "start_dir": "~/my-house/parents-room",
                        "end_dir": "~/my-house/parents-room",
                        "commands": ["echo hello", "echo HELLO", "echo Hello"],
                        "hints": [
                            "Use the command 'echo hello'"
                        ],
                        "next": [33, 1]
                    }
                ]
            },
            
            # Challenge 33: Going to the Farm
            {
                "title": "Journey to the Farm",
                "description": "Travel to the farm and explore",
                "commands_taught": ["cd", "ls"],
                "steps": [
                    {
                        "story": [
                            "Woah! You spoke aloud into the empty room!",
                            "",
                            "✅ You learnt the new power 'echo'!",
                            "",
                            "This command can probably be used to talk to people.",
                            "",
                            "Now let's head to ~ to find that farm!",
                            "Type 'cd' by itself to go to the Windy Road ~"
                        ],
                        "objective": "Go to the home directory",
                        "start_dir": "~/my-house/parents-room",
                        "end_dir": "~",
                        "commands": ["cd", "cd ~", "cd ~/"],
                        "hints": [
                            "Use 'cd' by itself to go to ~"
                        ],
                        "next": [33, 2]
                    },
                    {
                        "story": [
                            "You are back on the windy road, which stretches endlessly in both directions.",
                            "Look around."
                        ],
                        "objective": "Look around the windy road",
                        "start_dir": "~",
                        "end_dir": "~",
                        "commands": ["ls", "ls -a"],
                        "hints": [
                            "Look around with 'ls'."
                        ],
                        "next": [33, 3]
                    },
                    {
                        "story": [
                            "You notice a small remote farm in the distance.",
                            "",
                            "Let's go to the farm."
                        ],
                        "objective": "Go to the farm",
                        "start_dir": "~",
                        "end_dir": "~/farm",
                        "commands": ["cd farm", "cd farm/"],
                        "hints": [
                            "Use 'cd farm' to head to the farm."
                        ],
                        "next": [33, 4]
                    },
                    {
                        "story": [
                            "You walk up the path to the farm.",
                            "Look around."
                        ],
                        "objective": "Look around the farm",
                        "start_dir": "~/farm",
                        "end_dir": "~/farm",
                        "commands": ["ls"],
                        "hints": [
                            "Use 'ls' to look around."
                        ],
                        "next": [34, 1]
                    }
                ]
            },
            
            # Challenge 34: Exploring the Farm
            {
                "title": "Farm Exploration",
                "description": "Explore the farm and find the people",
                "commands_taught": ["ls", "cd"],
                "steps": [
                    {
                        "story": [
                            "You are in a farm, with a barn, a farmhouse and a large toolshed in sight.",
                            "The land is well tended and weed free, so there must be people about here.",
                            "",
                            "Look around and see if you can find someone to talk to.",
                            "Try looking in the barn."
                        ],
                        "objective": "Look in the barn for people",
                        "start_dir": "~/farm",
                        "end_dir": "~/farm",
                        "commands": ["ls barn", "ls barn/"],
                        "hints": [
                            "There is no one here. You should look somewhere else.",
                            "Have you looked in the barn yet?",
                            "Use 'ls barn' to look in the barn."
                        ],
                        "next": [34, 2]
                    },
                    {
                        "story": [
                            "In the barn, you see a woman tending some animals.",
                            "Walk into the barn so you can have a closer look."
                        ],
                        "objective": "Go into the barn",
                        "start_dir": "~/farm",
                        "end_dir": "~/farm/barn",
                        "commands": ["cd barn", "cd barn/"],
                        "hints": [
                            "Use 'cd barn' to walk into the barn."
                        ],
                        "next": [34, 3]
                    },
                    {
                        "story": [
                            "Examine everyone in the barn using the 'cat' command."
                        ],
                        "objective": "Talk to everyone in the barn",
                        "start_dir": "~/farm/barn",
                        "end_dir": "~/farm/barn",
                        "commands": ["cat Ruth", "cat Cobweb", "cat Trotter", "cat Daisy"],
                        "hints": [
                            "If you've forgotten who's in the barn, use 'ls' to remind yourself.",
                            "Use 'cat' with the names of the people and animals"
                        ],
                        "next": [35, 1]
                    }
                ]
            },
            
            # Challenge 35: Conversation with Ruth
            {
                "title": "Meeting Ruth",
                "description": "Have a conversation with Ruth using the echo command",
                "commands_taught": ["echo"],
                "steps": [
                    {
                        "story": [
                            "🐴 Cobweb: \"Neiiigh.\"",
                            "",
                            "🐷 Trotter: \"Oink Oink.\"",
                            "",
                            "🐄 Daisy: \"Mooooooooo.\"",
                            "",
                            "👩 Ruth: \"Ah! Who are you?!\"",
                            "\"Do I know you? You look familiar...\"",
                            "\"Wait, you're Mum's kid, aren't you!\"",
                            "\"...Yes? Do you have a tongue?\"",
                            "\"Is your name not [your name]?\"",
                            "",
                            "Reply with 'echo yes' or 'echo no'."
                        ],
                        "objective": "Reply to Ruth's question",
                        "start_dir": "~/farm/barn",
                        "end_dir": "~/farm/barn",
                        "commands": ["echo yes", "echo Yes", "echo YES"],
                        "hints": [
                            "Use 'echo' to reply to her question.",
                            "Reply with yes by using 'echo yes'."
                        ],
                        "next": [35, 2]
                    },
                    {
                        "story": [
                            "👩 Ruth: \"Ah, I knew it!\"",
                            "\"So you live in that little house outside town?\"",
                            "",
                            "1: \"Yes\"",
                            "2: \"No\"",
                            "3: \"I don't know\"",
                            "",
                            "Use 'echo 1', 'echo 2' or 'echo 3' to reply with either option 1, 2 or 3."
                        ],
                        "objective": "Choose an option to reply",
                        "start_dir": "~/farm/barn",
                        "end_dir": "~/farm/barn",
                        "commands": ["echo 1", "echo 2", "echo 3"],
                        "hints": [
                            "Use 'echo 1', 'echo 2' or 'echo 3' to reply to Ruth."
                        ],
                        "next": [35, 3]
                    },
                    {
                        "story": [
                            "👩 Ruth: \"I thought so!\"",
                            "",
                            "\"Did you walk all the way from town? Did you see my husband there?",
                            "He's a pretty grumpy-man, he was travelling to town because of that big meeting with the Mayor.\"",
                            "",
                            "1: \"I'm sorry, he disappeared in front of me.\"",
                            "2: \"I didn't see your husband, but people have been disappearing in town.\"",
                            "3: \"I don't know anything.\"",
                            "",
                            "Respond with one of the following options using the echo command and option number."
                        ],
                        "objective": "Tell Ruth about her husband",
                        "start_dir": "~/farm/barn",
                        "end_dir": "~/farm/barn",
                        "commands": ["echo 1"],
                        "hints": [
                            "Use 'echo 1', 'echo 2' or 'echo 3' to reply."
                        ],
                        "next": [35, 4]
                    },
                    {
                        "story": [
                            "👩 Ruth: \"He disappeared in front of you?? Oh no! They've been saying on the radio that people have been going missing...what should I do?\"",
                            "",
                            "1: \"Some people survived by going into hiding.\"",
                            "2: \"I think you should go and look for your husband\""
                        ],
                        "objective": "Give Ruth advice",
                        "start_dir": "~/farm/barn",
                        "end_dir": "~/farm/barn",
                        "commands": ["echo 1"],
                        "hints": [
                            "Use 'echo 1' or 'echo 2' to reply."
                        ],
                        "next": [36, 1]
                    }
                ]
            },
            
            # Challenge 36: Finding the Toolshed
            {
                "title": "The Toolshed Discovery",
                "description": "Help Ruth find shelter-building tools",
                "commands_taught": ["cd", "ls"],
                "steps": [
                    {
                        "story": [
                            "👩 Ruth: \"Oh! That reminds me, my husband used to build special shelters to store crops in over winter.",
                            "I think he used a specific tool.",
                            "We should take a look in his toolshed to see if we can find it.\"",
                            "",
                            "Use the 'cd' command to go into the toolshed."
                        ],
                        "objective": "Go to the toolshed",
                        "start_dir": "~/farm/barn",
                        "end_dir": "~/farm/toolshed",
                        "commands": ["cd ../toolshed", "cd ~/farm/toolshed"],
                        "hints": [
                            "Go to the toolshed in one step using 'cd ../toolshed'"
                        ],
                        "modifications": [
                            {"action": "remove", "path": "~/farm/barn/Ruth"},
                            {"action": "add", "path": "~/farm/toolshed/Ruth", "type": "file", "content": "Ruth"}
                        ],
                        "next": [36, 2]
                    },
                    {
                        "story": [
                            "Ruth follows you into the toolshed. It's a very large space with tools lining the walls.",
                            "",
                            "👩 Ruth: \"Let's look around for anything that could be useful.\""
                        ],
                        "objective": "Look around the toolshed",
                        "start_dir": "~/farm/toolshed",
                        "end_dir": "~/farm/toolshed",
                        "commands": ["ls", "ls -a", "ls .", "ls ./", "ls -a .", "ls -a ./"],
                        "hints": [
                            "Use 'ls' to look around."
                        ],
                        "next": [36, 3]
                    },
                    {
                        "story": [
                            "👩 Ruth: \"Ah, look! There are some instructions with the word MKDIR on it.\"",
                            "\"What does it say?\"",
                            "",
                            "Examine the MKDIR instructions."
                        ],
                        "objective": "Read the MKDIR instructions",
                        "start_dir": "~/farm/toolshed",
                        "end_dir": "~/farm/toolshed",
                        "commands": ["cat MKDIR"],
                        "hints": [
                            "Ruth: \"...you are able to read, yes? You use 'cat' to read things.\"",
                            "Ruth: \"What do you kids learn in schools nowadays...\"",
                            "\"Just use 'cat MKDIR' to read the paper.\"",
                            "Use 'cat MKDIR' to read it."
                        ],
                        "next": [37, 1]
                    }
                ]
            },
            
            # Challenge 37: Learning mkdir Command
            {
                "title": "Building Shelters",
                "description": "Learn the mkdir command to create directories",
                "commands_taught": ["mkdir"],
                "steps": [
                    {
                        "story": [
                            "👩 Ruth: \"This says you can make something using the word 'mkdir'?\"",
                            "",
                            "Try making an igloo using 'mkdir igloo'.",
                            "",
                            "💡 NEW POWER: 'mkdir' followed by a word lets you create a shelter"
                        ],
                        "objective": "Create an igloo shelter",
                        "start_dir": "~/farm/toolshed",
                        "end_dir": "~/farm/toolshed",
                        "commands": ["mkdir igloo"],
                        "hints": [
                            "Create an igloo structure by using 'mkdir igloo'"
                        ],
                        "next": [37, 2]
                    },
                    {
                        "story": [
                            "Now have a look around and see what's changed."
                        ],
                        "objective": "Look around to see the new igloo",
                        "start_dir": "~/farm/toolshed",
                        "end_dir": "~/farm/toolshed",
                        "commands": ["ls", "ls -a", "ls .", "ls ./"],
                        "hints": [
                            "Look around using 'ls'."
                        ],
                        "next": [38, 1]
                    }
                ]
            }
        ]