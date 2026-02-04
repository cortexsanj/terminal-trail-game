#!/usr/bin/env python3
"""
Terminal Trail - Simplified Edition
Main entry point for the game
"""

import sys
import os
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from game_engine import GameEngine


def main():
    parser = argparse.ArgumentParser(description='Terminal Trail - Learn Linux commands through story')
    parser.add_argument('--challenge', '-c', type=int, default=None, 
                       help='Start from specific challenge (1-63)')
    parser.add_argument('--step', '-s', type=int, default=None,
                       help='Start from specific step within challenge')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode with extra information')
    
    args = parser.parse_args()
    
    # Validate challenge and step if provided
    if args.challenge is not None and (args.challenge < 1 or args.challenge > 63):
        print("Error: Challenge must be between 1 and 63")
        sys.exit(1)
    
    if args.step is not None and args.step < 1:
        print("Error: Step must be 1 or greater")
        sys.exit(1)
    
    # Create and start game engine
    try:
        game = GameEngine(debug=args.debug)
        game.start(challenge=args.challenge, step=args.step)
    except KeyboardInterrupt:
        print("\n\nThanks for playing Terminal Trail!")
        sys.exit(0)
    except Exception as e:
        if args.debug:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()