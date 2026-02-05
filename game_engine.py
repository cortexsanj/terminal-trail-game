"""
Terminal Trail Game Engine
Core game loop and challenge management
"""

import os
import sys
from pathlib import Path
from typing import Optional, Tuple

from story_manager import StoryManager
from file_system import GameFileSystem
from terminal_handler import TerminalHandler
from progress_tracker import ProgressTracker
from level_config import get_level_progress


class GameEngine:
    """Main game engine that orchestrates all components"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.current_challenge = 1
        self.current_step = 1
        self.running = True
        self.saved_progress = None
        
        # Chapter mapping based on challenge numbers
        self.chapters = {
            (1, 10): "Chapter 1: Home",
            (11, 20): "Chapter 2: Town",
            (21, 30): "Chapter 3: Woods",
            (31, 40): "Chapter 4: Cave",
            (41, 57): "Chapter 5: Permissions",
            (58, 63): "Chapter 6: Finale"
        }
        
        # Initialize components
        self.story_manager = StoryManager(debug=debug)
        self.file_system = GameFileSystem(debug=debug)
        self.terminal_handler = TerminalHandler(self.file_system, debug=debug)
        self.progress_tracker = ProgressTracker()
        
        # Load saved progress (but don't apply it yet)
        self.saved_progress = self.progress_tracker.load_progress()
    
    def start(self, challenge: int = None, step: int = None):
        """Start the game from specified challenge/step"""
        # If command line args provided, use those
        if challenge is not None:
            self.current_challenge = challenge
        if step is not None:
            self.current_step = step
        # Otherwise, check for saved progress and ask user
        elif self.saved_progress:
            saved_challenge = self.saved_progress.get('challenge', 1)
            saved_step = self.saved_progress.get('step', 1)
            
            # Don't ask if they're at the very beginning
            if saved_challenge > 1 or saved_step > 1:
                print("=" * 60)
                print(f"📁 Saved progress found!")
                print(f"   Challenge {saved_challenge}, Step {saved_step}")
                print("=" * 60)
                
                try:
                    response = input("\nWould you like to resume from where you left off? (y/n): ").strip().lower()
                    if response in ['y', 'yes']:
                        self.current_challenge = saved_challenge
                        self.current_step = saved_step
                        print("✅ Resuming from saved progress...\n")
                    else:
                        print("✅ Starting from the beginning...\n")
                        # Reset progress file
                        self.progress_tracker.reset_progress()
                except (EOFError, KeyboardInterrupt):
                    print("\n✅ Starting from the beginning...\n")
                    self.progress_tracker.reset_progress()
        
        self._print_welcome()
        self._game_loop()
    
    def _print_welcome(self):
        """Print welcome message and game instructions"""
        print("=" * 60)
        print("🎮 TERMINAL TRAIL - Learn Linux Commands Through Story 🎮")
        print("=" * 60)
        print()
        print("Welcome to Terminal Trail! You'll learn Linux commands by")
        print("playing through an interactive story. Type the commands")
        print("exactly as shown to progress through the adventure.")
        print()
        print("💡 Tips:")
        print("  • Type 'help' for available commands")
        print("  • Type 'hint' if you're stuck")
        print("  • Type 'quit' to exit the game")
        print("  • Use TAB for auto-completion")
        print()
        print(f"Starting Challenge {self.current_challenge}, Step {self.current_step}")
        print("=" * 60)
        print()
    
    def _game_loop(self):
        """Main game loop"""
        while self.running:
            try:
                # Load current challenge
                challenge_data = self.story_manager.load_challenge(
                    self.current_challenge, self.current_step
                )
                
                if not challenge_data:
                    print(f"🎉 Congratulations! You've completed all challenges!")
                    print("You've mastered the essential Linux commands!")
                    break
                
                # Setup file system for this challenge
                self.file_system.setup_challenge(
                    self.current_challenge, self.current_step
                )
                
                # Apply any file system modifications for this step
                modifications = challenge_data.get('modifications', [])
                if modifications:
                    self.file_system.apply_challenge_modifications(modifications)
                
                # Display story text
                self._display_story(challenge_data)
                
                # Run challenge
                success = self._run_challenge(challenge_data)
                
                if success:
                    # Save progress
                    self.progress_tracker.save_progress(
                        self.current_challenge, self.current_step
                    )
                    
                    # Move to next step/challenge
                    next_challenge, next_step = challenge_data.get('next', (None, None))
                    
                    if next_challenge is None:
                        print("🎉 Game completed! Well done!")
                        break
                    
                    self.current_challenge = next_challenge
                    self.current_step = next_step
                    
                    print("\n✅ Challenge completed! Moving to next step...")
                    try:
                        input("Press Enter to continue...")
                    except EOFError:
                        pass  # Handle EOF gracefully
                    print("\n" + "="*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\nGame paused. Type 'quit' to exit or continue playing.")
                continue
            except Exception as e:
                if self.debug:
                    import traceback
                    traceback.print_exc()
                else:
                    print(f"Error: {e}")
                break
    
    def _get_chapter_name(self, challenge: int) -> str:
        """Get the chapter name for a given challenge number"""
        for (start, end), chapter_name in self.chapters.items():
            if start <= challenge <= end:
                return chapter_name
        return "Unknown Chapter"
    
    def _display_story(self, challenge_data: dict):
        """Display the story text for current challenge"""
        story_text = challenge_data.get('story', [])
        
        # Get level information
        level_info = get_level_progress(self.current_challenge)
        
        # Show level, challenge, and chapter on same line
        chapter_name = self._get_chapter_name(self.current_challenge)
        print(f"{level_info['level_emoji']} Level {level_info['level_num']}: {level_info['level_name']} | "
              f"🎮 Challenge {self.current_challenge} ({level_info['challenge_position']}/{level_info['total_challenges']})")
        print("=" * 60)
        print()
        
        print("📖 STORY:")
        print("-" * 40)
        
        for line in story_text:
            # Simple color formatting (remove complex formatting for now)
            clean_line = self._clean_story_text(line)
            print(clean_line)
        
        print("-" * 40)
        print()
        
        # Show objective
        objective = challenge_data.get('objective', '')
        if objective:
            print(f"🎯 OBJECTIVE: {objective}")
            print()
    
    def _clean_story_text(self, text: str) -> str:
        """Clean story text of complex formatting"""
        # Remove color formatting codes for now
        import re
        # Remove {{color:text}} patterns
        text = re.sub(r'\{\{[^:}]+:([^}]+)\}\}', r'\\1', text)
        # Remove remaining {{ }} patterns
        text = re.sub(r'\{\{[^}]+\}\}', '', text)
        return text.strip()
    
    def _run_challenge(self, challenge_data: dict) -> bool:
        """Run the current challenge and return success status"""
        required_commands = challenge_data.get('commands', [])
        if isinstance(required_commands, str):
            required_commands = [required_commands]
        
        hints = challenge_data.get('hints', [])
        hint_index = 0
        
        start_dir = challenge_data.get('start_dir', '~')
        end_dir = challenge_data.get('end_dir', '~')
        
        # Set starting directory
        self.terminal_handler.set_current_directory(start_dir)
        
        print(f"💻 TERMINAL (Current directory: {self.terminal_handler.get_current_directory()})")
        print("Type your commands below:")
        
        # Track completed commands for multi-command challenges
        completed_commands = []
        
        # Special handling for challenges that require multiple different commands
        # (like talking to multiple people or moving multiple items)
        # Check if this is truly a multi-command challenge by looking at the objective
        objective_lower = challenge_data.get('objective', '').lower()
        story_text = ' '.join(challenge_data.get('story', [])).lower()
        
        # Patterns that indicate multi-command challenges
        multi_command_patterns = [
            "at least 2", "any 2", "both", "all", "2 different", "2 more",
            "3 food items", "move 3", "everyone", "one by one"
        ]
        
        is_multi_command_challenge = any(
            phrase in objective_lower or phrase in story_text 
            for phrase in multi_command_patterns
        )
        
        # For multi-command challenges, determine the required count
        if is_multi_command_challenge:
            # Try to extract the number from objective or story
            if any(phrase in objective_lower or phrase in story_text for phrase in ["at least 2", "any 2", "2 different", "2 more"]):
                required_count = 2
            elif "3 food items" in objective_lower or "move 3" in objective_lower:
                required_count = 3
            elif "everyone" in story_text or "one by one" in story_text:
                # For "move everyone" type challenges, require all commands
                required_count = len(required_commands)
            else:
                required_count = len(required_commands)
        else:
            required_count = 1
        
        while True:
            try:
                # Get user input
                prompt = f"{self.terminal_handler.get_prompt()} "
                user_input = input(prompt).strip()
                
                # Handle special commands
                if user_input.lower() == 'quit':
                    self.running = False
                    return False
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'hint':
                    if hint_index < len(hints):
                        print(f"💡 HINT: {hints[hint_index]}")
                        hint_index += 1
                    else:
                        print("💡 No more hints available!")
                    continue
                elif user_input == '':
                    continue
                
                # Execute command
                success, output = self.terminal_handler.execute_command(user_input)
                
                if output:
                    print(output)
                
                # Check if command matches requirements
                if user_input in required_commands and user_input not in completed_commands:
                    completed_commands.append(user_input)
                    
                    # Check if enough commands completed
                    if len(completed_commands) >= required_count:
                        # Also check directory requirement
                        current_dir = self.terminal_handler.get_current_directory()
                        if end_dir == current_dir or end_dir == '~':
                            return True
                    else:
                        remaining = required_count - len(completed_commands)
                        if remaining > 0:
                            print(f"✅ Good! {remaining} more command(s) to go.")
                
                # Special case: if command already completed (alternative syntax)
                elif user_input in required_commands and user_input in completed_commands:
                    # For single command challenges with alternatives, this is still success
                    if required_count == 1:
                        current_dir = self.terminal_handler.get_current_directory()
                        if end_dir == current_dir or end_dir == '~':
                            return True
                
                # If command failed, show hint
                if not success and hints and hint_index < len(hints):
                    print(f"💡 HINT: {hints[hint_index]}")
                    hint_index += 1
                
            except KeyboardInterrupt:
                print("\n(Type 'quit' to exit)")
                continue
    
    def _check_command_success(self, command: str, required_commands: list, end_dir: str) -> bool:
        """Check if the command satisfies the challenge requirements"""
        # Check if command matches any required command
        command_match = any(command == req_cmd for req_cmd in required_commands)
        
        # Check if in correct directory (for now, just check command match)
        # Directory checking can be added later for more complex challenges
        
        return command_match
    
    def _show_help(self):
        """Show available commands"""
        print("\n📚 AVAILABLE COMMANDS:")
        print("  ls          - List files and directories")
        print("  ls -a       - List all files (including hidden)")
        print("  cd <dir>    - Change to directory")
        print("  cat <file>  - Display file contents")
        print("  pwd         - Show current directory")
        print("  mkdir <dir> - Create directory")
        print("  mv <src> <dst> - Move/rename file")
        print("  rm <file>   - Remove file")
        print("  echo <text> - Print text")
        print()
        print("📋 GAME COMMANDS:")
        print("  help        - Show this help")
        print("  hint        - Get a hint")
        print("  quit        - Exit game")
        print()