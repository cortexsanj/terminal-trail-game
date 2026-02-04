#!/usr/bin/env python3
"""
Terminal Trail Installation Script
"""

import sys
import os
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} - Compatible")
    return True

def check_dependencies():
    """Check if all required modules are available"""
    required_modules = ['json', 'pathlib', 'subprocess', 'argparse']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing required modules: {', '.join(missing)}")
        return False
    
    print("✅ All required modules available")
    return True

def setup_directories():
    """Create necessary directories"""
    base_dir = Path(__file__).parent
    
    directories = [
        base_dir / "challenges",
        base_dir / "assets" / "story_files"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directory created: {directory}")
    
    return True

def test_installation():
    """Test that the installation works"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        from game_engine import GameEngine
        from story_manager import StoryManager
        from file_system import GameFileSystem
        from terminal_handler import TerminalHandler
        from progress_tracker import ProgressTracker
        
        print("✅ All modules import successfully")
        
        # Test basic functionality
        fs = GameFileSystem()
        result = fs.list_directory('~/my-house/my-room')
        if result and 'alarm' in result:
            print("✅ File system working")
        else:
            print("❌ File system test failed")
            return False
        
        # Test story manager
        sm = StoryManager()
        challenge = sm.load_challenge(1, 1)
        if challenge and challenge.get('title'):
            print("✅ Story manager working")
        else:
            print("❌ Story manager test failed")
            return False
        
        print("✅ Installation test passed")
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def create_launcher():
    """Create a launcher script"""
    base_dir = Path(__file__).parent
    launcher_path = base_dir / "play.py"
    
    launcher_content = '''#!/usr/bin/env python3
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
'''
    
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    # Make executable on Unix systems
    if hasattr(os, 'chmod'):
        os.chmod(launcher_path, 0o755)
    
    print(f"✅ Launcher created: {launcher_path}")
    return True

def main():
    """Main installation process"""
    print("🎮 Terminal Trail - Installation")
    print("=" * 40)
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Setup directories
    if not setup_directories():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        sys.exit(1)
    
    # Create launcher
    if not create_launcher():
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("🎉 Installation completed successfully!")
    print("\nTo play Terminal Trail:")
    print("  python3 main.py")
    print("  or")
    print("  python3 play.py")
    print("\nFor help:")
    print("  python3 main.py --help")
    print("\nTo run tests:")
    print("  python3 test_game.py")
    print("=" * 40)

if __name__ == "__main__":
    main()