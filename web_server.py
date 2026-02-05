#!/usr/bin/env python3
"""
Terminal Trail Web Server
FastAPI server with WebSocket support for browser-based terminal
Works locally and on AWS App Runner
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import asyncio
import json
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import game components
try:
    from game_engine import GameEngine
    from terminal_handler import TerminalHandler
    from file_system import GameFileSystem
    from level_config import get_level_progress
except ImportError as e:
    print(f"Error importing game components: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

app = FastAPI(title="Terminal Trail")

# Add CORS middleware for WebSocket support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS)
static_dir = Path(__file__).parent / "web_static"
static_dir.mkdir(exist_ok=True)

# Add startup event for logging
@app.on_event("startup")
async def startup_event():
    import logging
    logger = logging.getLogger("uvicorn")
    logger.info("=" * 60)
    logger.info("FastAPI application starting up")
    logger.info(f"Static directory: {static_dir}")
    logger.info(f"Static directory exists: {static_dir.exists()}")
    if static_dir.exists():
        files = list(static_dir.glob("*"))
        logger.info(f"Static files: {[f.name for f in files]}")
    logger.info("=" * 60)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class WebGameSession:
    """Manages a single game session over WebSocket"""
    
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.game_engine = GameEngine(debug=False)
        self.input_queue = asyncio.Queue()
        self.running = True
        
    async def send_output(self, text: str):
        """Send text output to browser - convert newlines for terminal"""
        # Convert \n to \r\n for proper terminal display
        formatted_text = text.replace('\n', '\r\n')
        await self.websocket.send_json({
            "type": "output",
            "data": formatted_text
        })
    
    async def send_prompt(self, prompt: str):
        """Send prompt to browser"""
        await self.websocket.send_json({
            "type": "prompt",
            "data": prompt
        })
    
    async def get_input(self) -> str:
        """Get input from browser"""
        return await self.input_queue.get()
    
    async def handle_input(self, data: str):
        """Handle input from browser"""
        await self.input_queue.put(data)


@app.get("/")
async def get_index():
    """Serve the main game page"""
    html_file = static_dir / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    
    # Return a basic HTML if file doesn't exist yet
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Terminal Trail</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Terminal Trail</h1>
        <p>Static files not found. Please create web_static/index.html</p>
        <p>Or run: python3 web_server.py --setup</p>
    </body>
    </html>
    """)


@app.get("/favicon.ico")
async def favicon():
    """Return empty favicon to avoid 404 errors"""
    return HTMLResponse(content="", status_code=204)


@app.get("/health")
async def health_check():
    """Health check endpoint for AWS App Runner"""
    return {"status": "healthy", "service": "terminal-trail"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for game communication"""
    import logging
    logger = logging.getLogger("uvicorn")
    
    try:
        logger.info("WebSocket connection attempt from client")
        await websocket.accept()
        logger.info("WebSocket connection accepted")
        
        session = WebGameSession(websocket)
        
        # Send welcome message
        await session.send_output("🎮 Connecting to Terminal Trail...\n")
        await session.send_output("=" * 60 + "\n")
        
        # Start game in background task
        game_task = asyncio.create_task(run_game_session(session))
        
        # Handle incoming messages
        while session.running:
            try:
                message = await websocket.receive_json()
                
                if message["type"] == "input":
                    await session.handle_input(message["data"])
                elif message["type"] == "ping":
                    await websocket.send_json({"type": "pong"})
                    
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected by client")
                session.running = False
                break
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                break
        
        # Cleanup
        game_task.cancel()
        
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            await websocket.close()
        except:
            pass


async def run_game_session(session: WebGameSession):
    """Run the actual game session with custom I/O"""
    
    try:
        # Initialize game components
        file_system = GameFileSystem(debug=False)
        terminal_handler = TerminalHandler(file_system, debug=False)
        
        from story_manager import StoryManager
        from progress_tracker import ProgressTracker
        
        story_manager = StoryManager(debug=False)
        progress_tracker = ProgressTracker()
        
        # Game state
        current_challenge = 1
        current_step = 1
        
        # Check for saved progress
        saved_progress = progress_tracker.load_progress()
        if saved_progress:
            saved_challenge = saved_progress.get('challenge', 1)
            saved_step = saved_progress.get('step', 1)
            
            # Ask if they want to resume (if not at beginning)
            if saved_challenge > 1 or saved_step > 1:
                await session.send_output("=" * 60 + "\n")
                await session.send_output(f"📁 Saved progress found!\n")
                await session.send_output(f"   Challenge {saved_challenge}, Step {saved_step}\n")
                await session.send_output("=" * 60 + "\n\n")
                await session.send_prompt("Would you like to resume from where you left off? (y/n): ")
                
                response = await session.get_input()
                if response.strip().lower() in ['y', 'yes']:
                    current_challenge = saved_challenge
                    current_step = saved_step
                    await session.send_output("✅ Resuming from saved progress...\n\n")
                else:
                    await session.send_output("✅ Starting from the beginning...\n\n")
                    progress_tracker.reset_progress()
        
        # Print welcome message
        await session.send_output("=" * 60 + "\n")
        await session.send_output("🎮 TERMINAL TRAIL - Learn Linux Commands Through Story 🎮\n")
        await session.send_output("=" * 60 + "\n\n")
        await session.send_output("Welcome to Terminal Trail! You'll learn Linux commands by\n")
        await session.send_output("playing through an interactive story. Type the commands\n")
        await session.send_output("exactly as shown to progress through the adventure.\n\n")
        await session.send_output("💡 Tips:\n")
        await session.send_output("  • Type 'help' for available commands\n")
        await session.send_output("  • Type 'hint' if you're stuck\n")
        await session.send_output("  • Type 'quit' to exit the game\n\n")
        await session.send_output(f"Starting Challenge {current_challenge}, Step {current_step}\n")
        await session.send_output("=" * 60 + "\n\n")
        
        # Main game loop
        while session.running:
            try:
                # Load current challenge
                challenge_data = story_manager.load_challenge(current_challenge, current_step)
                
                if not challenge_data:
                    await session.send_output("🎉 Congratulations! You've completed all challenges!\n")
                    await session.send_output("You've mastered the essential Linux commands!\n")
                    break
                
                # Setup file system for this challenge
                file_system.setup_challenge(current_challenge, current_step)
                
                # Apply modifications
                modifications = challenge_data.get('modifications', [])
                if modifications:
                    file_system.apply_challenge_modifications(modifications)
                
                # Display story
                await display_story(session, challenge_data, current_challenge, current_step)
                
                # Run challenge
                success = await run_challenge(session, challenge_data, terminal_handler, file_system)
                
                if success:
                    # Save progress
                    progress_tracker.save_progress(current_challenge, current_step)
                    
                    # Move to next step/challenge
                    next_challenge, next_step = challenge_data.get('next', (None, None))
                    
                    if next_challenge is None:
                        await session.send_output("\n🎉 Game completed! Well done!\n")
                        break
                    
                    current_challenge = next_challenge
                    current_step = next_step
                    
                    await session.send_output("\n✅ Challenge completed! Moving to next step...\n")
                    await session.send_prompt("Press Enter to continue...")
                    await session.get_input()
                    await session.send_output("\n" + "="*60 + "\n\n")
                
            except Exception as e:
                await session.send_output(f"\nError: {e}\n")
                import traceback
                traceback.print_exc()
                break
                
    except asyncio.CancelledError:
        pass
    except Exception as e:
        await session.send_output(f"Fatal error: {e}\n")
        import traceback
        traceback.print_exc()


async def display_story(session: WebGameSession, challenge_data: dict, challenge_num: int, step_num: int):
    """Display the story text for current challenge"""
    import re
    
    # Get level information
    level_info = get_level_progress(challenge_num)
    
    # Get chapter name
    chapters = {
        (1, 10): "Chapter 1: Home",
        (11, 20): "Chapter 2: Town",
        (21, 30): "Chapter 3: Woods",
        (31, 40): "Chapter 4: Cave",
        (41, 57): "Chapter 5: Permissions",
        (58, 63): "Chapter 6: Finale"
    }
    
    chapter_name = "Unknown Chapter"
    for (start, end), name in chapters.items():
        if start <= challenge_num <= end:
            chapter_name = name
            break
    
    story_text = challenge_data.get('story', [])
    
    # Display level and challenge info
    await session.send_output(f"{level_info['level_emoji']} Level {level_info['level_num']}: {level_info['level_name']} | "
                             f"🎮 Challenge {challenge_num} ({level_info['challenge_position']}/{level_info['total_challenges']})\n")
    await session.send_output("=" * 60 + "\n\n")
    
    await session.send_output("📖 STORY:\n")
    await session.send_output("-" * 40 + "\n")
    
    for line in story_text:
        # Clean story text of formatting
        clean_line = re.sub(r'\{\{[^:}]+:([^}]+)\}\}', r'\1', line)
        clean_line = re.sub(r'\{\{[^}]+\}\}', '', clean_line)
        await session.send_output(clean_line.strip() + "\n")
    
    await session.send_output("-" * 40 + "\n\n")
    
    # Show objective
    objective = challenge_data.get('objective', '')
    if objective:
        await session.send_output(f"🎯 OBJECTIVE: {objective}\n\n")


async def run_challenge(session: WebGameSession, challenge_data: dict, terminal_handler: TerminalHandler, file_system: GameFileSystem) -> bool:
    """Run the current challenge and return success status"""
    required_commands = challenge_data.get('commands', [])
    if isinstance(required_commands, str):
        required_commands = [required_commands]
    
    hints = challenge_data.get('hints', [])
    hint_index = 0
    
    start_dir = challenge_data.get('start_dir', '~')
    end_dir = challenge_data.get('end_dir', '~')
    
    # Set starting directory
    terminal_handler.set_current_directory(start_dir)
    
    await session.send_output(f"💻 TERMINAL (Current directory: {terminal_handler.get_current_directory()})\n")
    await session.send_output("Type your commands below:\n")
    
    # Track completed commands
    completed_commands = []
    
    # Determine if multi-command challenge
    objective_lower = challenge_data.get('objective', '').lower()
    story_text = ' '.join(challenge_data.get('story', [])).lower()
    
    multi_command_patterns = [
        "at least 2", "any 2", "both", "all", "2 different", "2 more",
        "3 food items", "move 3", "everyone", "one by one"
    ]
    
    is_multi_command_challenge = any(
        phrase in objective_lower or phrase in story_text 
        for phrase in multi_command_patterns
    )
    
    if is_multi_command_challenge:
        if any(phrase in objective_lower or phrase in story_text for phrase in ["at least 2", "any 2", "2 different", "2 more"]):
            required_count = 2
        elif "3 food items" in objective_lower or "move 3" in objective_lower:
            required_count = 3
        elif "everyone" in story_text or "one by one" in story_text:
            required_count = len(required_commands)
        else:
            required_count = len(required_commands)
    else:
        required_count = 1
    
    while True:
        # Get user input
        prompt = f"{terminal_handler.get_prompt()} "
        await session.send_prompt(prompt)
        user_input = (await session.get_input()).strip()
        
        # Handle special commands
        if user_input.lower() == 'quit':
            session.running = False
            return False
        elif user_input.lower() == 'help':
            await show_help(session)
            continue
        elif user_input.lower() == 'hint':
            if hint_index < len(hints):
                await session.send_output(f"💡 HINT: {hints[hint_index]}\n")
                hint_index += 1
            else:
                await session.send_output("💡 No more hints available!\n")
            continue
        elif user_input == '':
            continue
        
        # Execute command
        success, output = terminal_handler.execute_command(user_input)
        
        if output:
            await session.send_output(output + "\n")
        
        # Check if command matches requirements
        if user_input in required_commands and user_input not in completed_commands:
            completed_commands.append(user_input)
            
            if len(completed_commands) >= required_count:
                current_dir = terminal_handler.get_current_directory()
                if end_dir == current_dir or end_dir == '~':
                    return True
            else:
                remaining = required_count - len(completed_commands)
                if remaining > 0:
                    await session.send_output(f"✅ Good! {remaining} more command(s) to go.\n")
        
        elif user_input in required_commands and user_input in completed_commands:
            if required_count == 1:
                current_dir = terminal_handler.get_current_directory()
                if end_dir == current_dir or end_dir == '~':
                    return True
        
        if not success and hints and hint_index < len(hints):
            await session.send_output(f"💡 HINT: {hints[hint_index]}\n")
            hint_index += 1


async def show_help(session: WebGameSession):
    """Show available commands"""
    await session.send_output("\n📚 AVAILABLE COMMANDS:\n")
    await session.send_output("  ls          - List files and directories\n")
    await session.send_output("  ls -a       - List all files (including hidden)\n")
    await session.send_output("  cd <dir>    - Change to directory\n")
    await session.send_output("  cat <file>  - Display file contents\n")
    await session.send_output("  pwd         - Show current directory\n")
    await session.send_output("  mkdir <dir> - Create directory\n")
    await session.send_output("  mv <src> <dst> - Move/rename file\n")
    await session.send_output("  rm <file>   - Remove file\n")
    await session.send_output("  echo <text> - Print text\n")
    await session.send_output("\n📋 GAME COMMANDS:\n")
    await session.send_output("  help        - Show this help\n")
    await session.send_output("  hint        - Get a hint\n")
    await session.send_output("  quit        - Exit game\n\n")


def create_static_files():
    """Create the static HTML/CSS/JS files"""
    
    # Create index.html
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal Trail - Learn Linux Commands</title>
    <link rel="stylesheet" href="/static/terminal.css">
    <script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-left">
                <h1>🎮 Terminal Trail</h1>
                <p>Learn Linux Commands Through Story</p>
                <div id="level-indicator" class="level-indicator">
                    <span id="level-text">Level 1: First Steps</span>
                </div>
            </div>
            <div class="header-right">
                <div class="tips">
                    <div class="tips-title">💡 Tips:</div>
                    <ul>
                        <li>Type 'help' for available commands</li>
                        <li>Type 'hint' if you're stuck</li>
                        <li>Type 'quit' to exit the game</li>
                    </ul>
                </div>
            </div>
        </div>
        <div id="terminal-container"></div>
        <div class="footer">
            <p>Type commands to play • Press Ctrl+C to interrupt</p>
        </div>
    </div>
    <script src="/static/terminal.js"></script>
</body>
</html>
"""
    
    # Create terminal.css
    css_content = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Courier New', monospace;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.container {
    width: 100%;
    max-width: 1080px;
    background: rgba(0, 0, 0, 0.8);
    border-radius: 10px;
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
    overflow: hidden;
}

.header {
    background: rgba(0, 0, 0, 0.5);
    padding: 20px;
    border-bottom: 2px solid #00ff00;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
}

.header-left {
    flex: 1;
    min-width: 0;
}

.header-right {
    flex-shrink: 0;
}

.header h1 {
    color: #00ff00;
    font-size: 2em;
    margin-bottom: 10px;
    text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.header p {
    color: #00ff00;
    opacity: 0.8;
    margin-bottom: 10px;
}

.level-indicator {
    margin-top: 10px;
    padding: 8px 16px;
    background: rgba(0, 255, 0, 0.1);
    border: 1px solid #00ff00;
    border-radius: 5px;
    display: inline-block;
}

.level-indicator span {
    color: #00ff00;
    font-weight: bold;
    font-size: 0.95em;
}

.tips {
    background: rgba(0, 255, 0, 0.05);
    border: 1px solid rgba(0, 255, 0, 0.3);
    border-radius: 5px;
    padding: 12px 16px;
    min-width: 280px;
}

.tips-title {
    color: #00ff00;
    font-weight: bold;
    margin-bottom: 8px;
    font-size: 0.95em;
}

.tips ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.tips li {
    color: #00ff00;
    opacity: 0.85;
    font-size: 0.85em;
    line-height: 1.6;
    padding-left: 12px;
    position: relative;
}

.tips li:before {
    content: "•";
    position: absolute;
    left: 0;
    color: #00ff00;
}

#terminal-container {
    padding: 20px;
    background: #000;
}

.xterm {
    height: 540px;
    padding: 10px;
}

.xterm-viewport {
    background-color: #000 !important;
}

.footer {
    background: rgba(0, 0, 0, 0.5);
    padding: 15px;
    text-align: center;
    border-top: 2px solid #00ff00;
    color: #00ff00;
    font-size: 0.9em;
    opacity: 0.7;
}

/* Loading animation */
.loading {
    color: #00ff00;
    text-align: center;
    padding: 20px;
}

.loading::after {
    content: '...';
    animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
    0%, 20% { content: '.'; }
    40% { content: '..'; }
    60%, 100% { content: '...'; }
}

/* Responsive */
@media (max-width: 768px) {
    body {
        padding: 10px;
        align-items: flex-start;
    }
    
    .container {
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .header {
        padding: 15px 10px;
        flex-direction: column;
        gap: 15px;
    }
    
    .header-right {
        width: 100%;
    }
    
    .tips {
        min-width: 0;
        width: 100%;
    }
    
    .header h1 {
        font-size: 1.3em;
    }
    
    .header p {
        font-size: 0.85em;
    }
    
    .level-indicator {
        padding: 6px 12px;
        margin-top: 8px;
    }
    
    .level-indicator span {
        font-size: 0.85em;
    }
    
    .tips-title {
        font-size: 0.9em;
    }
    
    .tips li {
        font-size: 0.8em;
    }
    
    #terminal-container {
        padding: 10px;
    }
    
    .xterm {
        height: 400px;
        padding: 5px;
    }
    
    .footer {
        padding: 10px;
        font-size: 0.8em;
    }
}

/* Extra small devices (phones in portrait) */
@media (max-width: 480px) {
    body {
        padding: 5px;
    }
    
    .container {
        margin: 5px 0;
    }
    
    .header {
        padding: 12px 8px;
    }
    
    .header h1 {
        font-size: 1.1em;
    }
    
    .header p {
        font-size: 0.75em;
    }
    
    .level-indicator {
        padding: 5px 10px;
    }
    
    .level-indicator span {
        font-size: 0.75em;
    }
    
    .tips {
        padding: 10px 12px;
    }
    
    .tips-title {
        font-size: 0.85em;
    }
    
    .tips li {
        font-size: 0.75em;
        line-height: 1.5;
    }
    
    .xterm {
        height: 350px;
    }
    
    .footer p {
        font-size: 0.7em;
    }
}
"""
    
    # Create terminal.js
    js_content = """// Terminal Trail - Browser Client
// Detect mobile and adjust terminal settings
const isMobile = window.innerWidth <= 768;
const fontSize = isMobile ? 12 : 14;

const term = new Terminal({
    cursorBlink: true,
    fontSize: fontSize,
    fontFamily: 'Courier New, monospace',
    theme: {
        background: '#000000',
        foreground: '#00ff00',
        cursor: '#00ff00',
        cursorAccent: '#000000',
        selection: 'rgba(0, 255, 0, 0.3)',
        black: '#000000',
        red: '#ff0000',
        green: '#00ff00',
        yellow: '#ffff00',
        blue: '#0000ff',
        magenta: '#ff00ff',
        cyan: '#00ffff',
        white: '#ffffff',
        brightBlack: '#808080',
        brightRed: '#ff8080',
        brightGreen: '#80ff80',
        brightYellow: '#ffff80',
        brightBlue: '#8080ff',
        brightMagenta: '#ff80ff',
        brightCyan: '#80ffff',
        brightWhite: '#ffffff'
    }
});

// Open terminal in container
term.open(document.getElementById('terminal-container'));

// Fit terminal to container
function fitTerminal() {
    const container = document.getElementById('terminal-container');
    const dims = {
        cols: Math.floor(container.offsetWidth / (fontSize * 0.6)),
        rows: Math.floor(container.offsetHeight / (fontSize * 1.5))
    };
    term.resize(dims.cols, dims.rows);
}

// Fit on load and resize
window.addEventListener('load', fitTerminal);
window.addEventListener('resize', fitTerminal);

// WebSocket connection
let ws = null;
let currentInput = '';
let isWaitingForInput = false;

// Function to update level indicator
function updateLevelIndicator(text) {
    const levelText = document.getElementById('level-text');
    if (levelText && text) {
        // Extract level info from terminal output
        const levelMatch = text.match(/Level (\\d+): ([^|]+)/);
        if (levelMatch) {
            const levelNum = levelMatch[1];
            const levelName = levelMatch[2].trim();
            levelText.textContent = `Level ${levelNum}: ${levelName}`;
        }
    }
}

function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    term.writeln('\\x1b[32mConnecting to Terminal Trail...\\x1b[0m');
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        term.writeln('\\x1b[32m✓ Connected!\\x1b[0m\\r\\n');
    };
    
    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        
        if (message.type === 'output') {
            const output = message.data.replace(/\\n/g, '\\r\\n');
            term.write(output);
            // Update level indicator if level info is in the output
            updateLevelIndicator(message.data);
        } else if (message.type === 'prompt') {
            term.write(message.data);
            isWaitingForInput = true;
        } else if (message.type === 'pong') {
            // Keep-alive response
        }
    };
    
    ws.onerror = (error) => {
        term.writeln('\\r\\n\\x1b[31m✗ Connection error\\x1b[0m\\r\\n');
        console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
        term.writeln('\\r\\n\\x1b[33m✗ Disconnected from server\\x1b[0m\\r\\n');
        term.writeln('\\x1b[33mRefresh the page to reconnect\\x1b[0m\\r\\n');
    };
}

// Handle terminal input
term.onData((data) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        return;
    }
    
    // Handle special keys
    if (data === '\\r') { // Enter
        term.write('\\r\\n');
        
        if (isWaitingForInput) {
            ws.send(JSON.stringify({
                type: 'input',
                data: currentInput
            }));
            currentInput = '';
            isWaitingForInput = false;
        }
    } else if (data === '\\u007F') { // Backspace
        if (currentInput.length > 0) {
            currentInput = currentInput.slice(0, -1);
            term.write('\\b \\b');
        }
    } else if (data === '\\u0003') { // Ctrl+C
        term.write('^C\\r\\n');
        currentInput = '';
        ws.send(JSON.stringify({
            type: 'input',
            data: ''
        }));
    } else if (data >= String.fromCharCode(0x20) && data <= String.fromCharCode(0x7E)) {
        // Printable characters
        currentInput += data;
        term.write(data);
    }
});

// Keep-alive ping every 30 seconds
setInterval(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'ping' }));
    }
}, 30000);

// Connect on load
connect();

// Handle window resize
window.addEventListener('resize', () => {
    // Terminal will auto-resize
});
"""
    
    # Write files
    (static_dir / "index.html").write_text(html_content)
    (static_dir / "terminal.css").write_text(css_content)
    (static_dir / "terminal.js").write_text(js_content)
    
    print("✓ Created web_static/index.html")
    print("✓ Created web_static/terminal.css")
    print("✓ Created web_static/terminal.js")


if __name__ == "__main__":
    import uvicorn
    import os
    import logging
    
    # Configure logging for App Runner
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("=" * 60)
        logger.info("🎮 Terminal Trail Web Server Starting")
        logger.info("=" * 60)
        
        # Check if --setup flag
        if "--setup" in sys.argv:
            logger.info("Running setup mode...")
            create_static_files()
            logger.info("Setup complete!")
            sys.exit(0)
        
        # Log environment info
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Current directory: {os.getcwd()}")
        logger.info(f"Files in current directory: {os.listdir('.')}")
        
        # Check for required directories
        required_dirs = ['challenges', 'assets']
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                count = len(os.listdir(dir_name))
                logger.info(f"✓ Found {dir_name}/ with {count} items")
            else:
                logger.error(f"✗ Missing required directory: {dir_name}/")
                sys.exit(1)
        
        # Create static files if they don't exist
        if not (static_dir / "index.html").exists():
            logger.info("Static files not found. Creating them...")
            try:
                create_static_files()
                logger.info("✓ Static files created successfully")
            except Exception as e:
                logger.error(f"✗ Failed to create static files: {e}")
                import traceback
                traceback.print_exc()
                sys.exit(1)
        else:
            logger.info("✓ Static files already exist")
        
        # Get port from environment or default to 8000
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"Port: {port}")
        logger.info(f"Host: 0.0.0.0 (all interfaces)")
        
        # Test import of game components
        logger.info("Testing game component imports...")
        try:
            from story_manager import StoryManager
            from progress_tracker import ProgressTracker
            logger.info("✓ All game components imported successfully")
        except Exception as e:
            logger.error(f"✗ Failed to import game components: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        logger.info("=" * 60)
        logger.info("Starting uvicorn server...")
        logger.info("=" * 60)
        
        # Run server
        uvicorn.run(
            app, 
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"✗ Fatal error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
