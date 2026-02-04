#!/usr/bin/env python3
"""
Terminal Trail Launcher
Quick way to start the game
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import main

if __name__ == "__main__":
    main()
