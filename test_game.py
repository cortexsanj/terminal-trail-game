#!/usr/bin/env python3
"""
Test script to demonstrate Terminal Trail functionality
"""

import subprocess
import sys
from pathlib import Path

def test_basic_functionality():
    """Test basic game functionality"""
    print("🧪 Testing Terminal Trail Basic Functionality")
    print("=" * 50)
    
    # Test 1: Help command
    print("\n1. Testing help command...")
    result = subprocess.run([sys.executable, "main.py", "--help"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Help command works")
    else:
        print("❌ Help command failed")
        return False
    
    # Test 2: File system
    print("\n2. Testing file system...")
    test_code = """
from file_system import GameFileSystem
fs = GameFileSystem()
result = fs.list_directory('~/my-house/my-room')
print(f"Room contents: {result}")
assert result == ['alarm', 'bed', 'wardrobe', 'shelves']
print("✅ File system works correctly")
"""
    
    result = subprocess.run([sys.executable, "-c", test_code], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print("❌ File system test failed")
        print(result.stderr)
        return False
    
    # Test 3: Terminal handler
    print("\n3. Testing terminal handler...")
    test_code = """
from file_system import GameFileSystem
from terminal_handler import TerminalHandler
fs = GameFileSystem()
th = TerminalHandler(fs)
th.set_current_directory('~/my-house/my-room')
success, output = th.execute_command('ls')
print(f"Command output: {output}")
assert success == True
assert 'alarm' in output
print("✅ Terminal handler works correctly")
"""
    
    result = subprocess.run([sys.executable, "-c", test_code], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print("❌ Terminal handler test failed")
        print(result.stderr)
        return False
    
    # Test 4: Story manager
    print("\n4. Testing story manager...")
    test_code = """
from story_manager import StoryManager
sm = StoryManager()
challenge = sm.load_challenge(1, 1)
print(f"Challenge title: {challenge['title']}")
assert challenge['title'] == 'Wake Up Call'
print("✅ Story manager works correctly")
"""
    
    result = subprocess.run([sys.executable, "-c", test_code], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print("❌ Story manager test failed")
        print(result.stderr)
        return False
    
    print("\n🎉 All tests passed! Terminal Trail is working correctly.")
    return True

def demo_game_session():
    """Demonstrate a game session"""
    print("\n" + "=" * 50)
    print("🎮 DEMO: Playing through first few challenges")
    print("=" * 50)
    
    # Commands to demonstrate the first few challenges
    commands = [
        "ls",           # Challenge 1: Look around
        "cat alarm",    # Challenge 2: Examine alarm
        "ls wardrobe/", # Challenge 2 step 2: Look in wardrobe
        "cat wardrobe/t-shirt",  # Challenge 3: Examine t-shirt
        "quit"
    ]
    
    print("Commands to be executed:")
    for i, cmd in enumerate(commands, 1):
        print(f"  {i}. {cmd}")
    
    print("\nRunning demo...")
    
    # Create input string
    input_string = "\n".join(commands)
    
    # Run the game with the commands
    result = subprocess.run([sys.executable, "main.py"], 
                          input=input_string, 
                          capture_output=True, 
                          text=True)
    
    if result.returncode == 0:
        print("✅ Demo completed successfully!")
        print("\nGame output preview:")
        lines = result.stdout.split('\n')
        # Show first 20 lines and last 10 lines
        for line in lines[:20]:
            print(line)
        if len(lines) > 30:
            print("... (output truncated) ...")
            for line in lines[-10:]:
                print(line)
    else:
        print("❌ Demo failed")
        print("Error:", result.stderr)

def main():
    """Run all tests and demo"""
    print("Terminal Trail - Test Suite")
    print("=" * 50)
    
    # Change to the correct directory
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)
    
    # Run tests
    if test_basic_functionality():
        demo_game_session()
    else:
        print("❌ Basic functionality tests failed. Skipping demo.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Terminal Trail is ready to play!")
    print("Run: python3 main.py")
    print("=" * 50)

if __name__ == "__main__":
    main()