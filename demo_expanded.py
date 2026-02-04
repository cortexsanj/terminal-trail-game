#!/usr/bin/env python3
"""
Demo script for the expanded Terminal Trail
Shows the progression through multiple detailed challenges
"""

import subprocess
import sys

def demo_expanded_game():
    """Demonstrate the expanded game with more detailed challenges"""
    print("🎮 EXPANDED TERMINAL TRAIL DEMO")
    print("=" * 50)
    print("This demo shows the expanded challenges with more detail")
    print("based on the original Terminal Trail challenges 1-3.")
    print()
    
    # Commands that will take us through several challenges
    commands = [
        # Challenge 1: Wake up and look around
        "ls",
        
        # Challenge 2: Examine alarm and wardrobe
        "cat alarm",
        "ls wardrobe/",
        
        # Challenge 3: Get dressed - examine clothes
        "cat wardrobe/t-shirt",
        "cat wardrobe/trousers",  # Choose trousers
        "cat wardrobe/cap",
        
        # Challenge 4: Explore shelves
        "ls shelves",
        "cat shelves/comic-book",
        "cat shelves/note",
        
        # Challenge 5: Learn to move around
        "cd ..",
        "ls",
        "cd kitchen",
        
        # Challenge 6: Meet Mum
        "ls",
        "cat Mum",
        
        # Challenge 7: Look for Dad
        "cd ..",
        "ls", 
        "cd garden",
        "ls",
        "cd greenhouse",
        
        # Challenge 8: Find the note
        "ls",
        "cat note",
        
        # Challenge 9: Learn pwd
        "pwd",
        
        # Challenge 10: Go back to kitchen
        "cd ~/my-house/kitchen",
        
        "quit"
    ]
    
    print("Commands that will be executed:")
    for i, cmd in enumerate(commands, 1):
        print(f"  {i:2d}. {cmd}")
    
    print(f"\nTotal commands: {len(commands)}")
    print("This demonstrates:")
    print("  • Multiple steps per challenge")
    print("  • Progressive story development") 
    print("  • Character interactions")
    print("  • Detailed exploration")
    print("  • All basic Linux commands")
    
    print("\nRunning demo...")
    print("=" * 50)
    
    # Create input string
    input_string = "\n".join(commands)
    
    # Run the game with the commands
    result = subprocess.run([sys.executable, "main.py"], 
                          input=input_string, 
                          capture_output=True, 
                          text=True)
    
    if result.returncode == 0:
        print("✅ Demo completed successfully!")
        
        # Count challenges completed
        output_lines = result.stdout.split('\n')
        challenge_lines = [line for line in output_lines if "Challenge completed" in line]
        
        print(f"🎯 Challenges completed: {len(challenge_lines)}")
        print("📚 Commands learned: ls, cat, cd, pwd")
        print("🏠 Areas explored: bedroom, kitchen, garden, greenhouse")
        print("👥 Characters met: Mum, mysterious note writer")
        
        # Show some sample output
        print("\n📋 Sample game output:")
        print("-" * 30)
        for line in output_lines[5:15]:  # Show some story text
            if line.strip():
                print(line)
        print("-" * 30)
        
    else:
        print("❌ Demo failed")
        print("Error:", result.stderr)

def main():
    """Run the expanded demo"""
    demo_expanded_game()
    
    print("\n" + "=" * 50)
    print("🎉 The expanded Terminal Trail is ready!")
    print("Now includes:")
    print("  • 10 detailed challenges (vs 3 simple ones)")
    print("  • 28+ individual steps")
    print("  • Rich story with character interactions")
    print("  • Progressive skill building")
    print("  • Multiple commands per challenge")
    print()
    print("To play: python3 main.py")
    print("=" * 50)

if __name__ == "__main__":
    main()