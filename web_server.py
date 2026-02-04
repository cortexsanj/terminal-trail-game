#!/usr/bin/env python3
"""
Terminal Trail Web Server
FastAPI server with HTTP polling for browser-based terminal
Works on AWS App Runner (no WebSocket support needed)
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import asyncio
import json
import sys
import os
import uuid
from typing import Dict, Optional
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import game components
try:
    from game_engine import GameEngine
    from terminal_handler import TerminalHandler
    from file_system import GameFileSystem
except ImportError as e:
    print(f"Error importing game components: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

app = FastAPI(title="Terminal Trail")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


# Session management
class GameSession:
    """Manages a single game session with HTTP polling"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.game_engine = GameEngine(debug=False)
        self.input_queue = asyncio.Queue()
        self.output_buffer = []
        self.running = True
        self.last_activity = datetime.now()
        self.game_task = None
        
    async def send_output(self, text: str):
        """Buffer text output for polling"""
        self.output_buffer.append(text)
        self.last_activity = datetime.now()
    
    async def send_prompt(self, prompt: str):
        """Buffer prompt for polling"""
        self.output_buffer.append(prompt)
        self.last_activity = datetime.now()
    
    async def get_input(self) -> str:
        """Get input from queue"""
        return await self.input_queue.get()
    
    async def handle_input(self, data: str):
        """Handle input from browser"""
        await self.input_queue.put(data)
        self.last_activity = datetime.now()
    
    def get_buffered_output(self) -> str:
        """Get and clear output buffer"""
        if self.output_buffer:
            output = "".join(self.output_buffer)
            self.output_buffer = []
            self.last_activity = datetime.now()
            return output
        return ""


# Store active sessions
sessions: Dict[str, GameSession] = {}

# Cleanup old sessions periodically
async def cleanup_sessions():
    """Remove inactive sessions after 30 minutes"""
    while True:
        await asyncio.sleep(300)  # Check every 5 minutes
        now = datetime.now()
        to_remove = []
        for session_id, session in sessions.items():
            if now - session.last_activity > timedelta(minutes=30):
                to_remove.append(session_id)
                if session.game_task:
                    session.game_task.cancel()
        
        for session_id in to_remove:
            del sessions[session_id]
            print(f"Cleaned up inactive session: {session_id}")

@app.on_event("startup")
async def start_cleanup():
    asyncio.create_task(cleanup_sessions())


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


@app.get("/health")
async def health_check():
    """Health check endpoint for AWS App Runner"""
    return {"status": "healthy", "service": "terminal-trail"}


@app.post("/api/session/start")
async def start_session():
    """Start a new game session"""
    session_id = str(uuid.uuid4())
    session = GameSession(session_id)
    sessions[session_id] = session
    
    # Start game in background
    session.game_task = asyncio.create_task(run_game_session(session))
    
    return {"session_id": session_id}


@app.post("/api/session/{session_id}/input")
async def send_input(session_id: str, data: dict):
    """Send user input to game session"""
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    user_input = data.get("input", "")
    await session.handle_input(user_input)
    
    return {"status": "ok"}


@app.get("/api/session/{session_id}/output")
async def get_output(session_id: str):
    """Poll for new output from game session"""
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    output = session.get_buffered_output()
    return {
        "output": output,
        "running": session.running
    }


async def run_game_session(session: GameSession):
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
                
                if response.lower().strip() == 'y':
                    current_challenge = saved_challenge
                    current_step = saved_step
                    await session.send_output("\n✓ Resuming from saved progress...\n\n")
                else:
                    # Reset progress
                    progress_tracker.save_progress(1, 1)
                    await session.send_output("\n✓ Starting fresh adventure...\n\n")
        
        # Welcome message
        await session.send_output("\n" + "=" * 60 + "\n")
        await session.send_output("🎮 TERMINAL TRAIL 🎮\n")
        await session.send_output("=" * 60 + "\n\n")
        await session.send_output("Welcome to Terminal Trail!\n")
        await session.send_output("Learn Linux commands through an interactive story.\n\n")
        
        # Get chapter info
        def get_chapter_info(challenge_num):
            if challenge_num <= 10:
                return "Chapter 1: Home"
            elif challenge_num <= 20:
                return "Chapter 2: Town"
            elif challenge_num <= 30:
                return "Chapter 3: Woods"
            elif challenge_num <= 40:
                return "Chapter 4: Cave"
            elif challenge_num <= 57:
                return "Chapter 5: Permissions"
            else:
                return "Chapter 6: Finale"
        
        # Main game loop
        while session.running and current_challenge <= 63:
            try:
                # Load challenge
                challenge_file = Path(f"challenges/challenge_{current_challenge:02d}.json")
                if not challenge_file.exists():
                    await session.send_output(f"\n❌ Challenge file not found: {challenge_file}\n")
                    break
                
                with open(challenge_file) as f:
                    challenge_data = json.load(f)
                
                steps = challenge_data.get('steps', [])
                if current_step > len(steps):
                    # Move to next challenge
                    current_challenge += 1
                    current_step = 1
                    progress_tracker.save_progress(current_challenge, current_step)
                    continue
                
                step = steps[current_step - 1]
                
                # Display chapter and challenge info
                chapter_info = get_chapter_info(current_challenge)
                await session.send_output("\n" + "=" * 60 + "\n")
                await session.send_output(f"📚 {chapter_info} | 🎮 Challenge {current_challenge}\n")
                await session.send_output("=" * 60 + "\n\n")
                
                # Display story
                story_text = step.get('story', '')
                if story_text:
                    # Story can be a list or string
                    if isinstance(story_text, list):
                        formatted_story = "\n".join(story_text)
                    else:
                        formatted_story = story_text
                    await session.send_output(formatted_story + "\n\n")
                
                # Display hint if available
                hint = step.get('hint', '')
                if hint:
                    await session.send_output(f"💡 Hint: {hint}\n\n")
                
                # Get command
                await session.send_prompt("$ ")
                command = await session.get_input()
                
                # Echo command
                await session.send_output(command + "\n")
                
                # Check for quit
                if command.lower().strip() in ['quit', 'exit']:
                    await session.send_output("\n� Thanks for playing Terminal Trail!\n")
                    await session.send_output("Your progress has been saved.\n\n")
                    session.running = False
                    break
                
                # Process command
                result = terminal_handler.execute_command(command)
                await session.send_output(result + "\n")
                
                # Check if command is correct
                expected_commands = step.get('command', [])
                if isinstance(expected_commands, str):
                    expected_commands = [expected_commands]
                
                command_correct = False
                for expected in expected_commands:
                    if command.strip() == expected.strip():
                        command_correct = True
                        break
                
                if command_correct:
                    await session.send_output("\n✓ Correct! Moving to next step...\n")
                    current_step += 1
                    progress_tracker.save_progress(current_challenge, current_step)
                else:
                    await session.send_output("\n❌ That's not quite right. Try again!\n")
                
            except Exception as e:
                await session.send_output(f"\n❌ Error: {e}\n")
                import traceback
                traceback.print_exc()
        
        # Game complete
        if current_challenge > 63:
            await session.send_output("\n" + "=" * 60 + "\n")
            await session.send_output("🎉 CONGRATULATIONS! 🎉\n")
            await session.send_output("=" * 60 + "\n\n")
            await session.send_output("You've completed Terminal Trail!\n")
            await session.send_output("You're now a Linux command line expert!\n\n")
        
        session.running = False
        
    except Exception as e:
        await session.send_output(f"\n❌ Fatal error: {e}\n")
        import traceback
        traceback.print_exc()
        session.running = False


def create_static_files():
    """Create HTML, CSS, and JS files for the web interface"""
    
    # Create index.html with HTTP polling
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
            <h1>🎮 Terminal Trail</h1>
            <p>Learn Linux commands through an interactive story</p>
        </div>
        <div id="terminal-container"></div>
        <div class="footer">
            <p>Type commands and press Enter | Type 'quit' to exit</p>
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
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #00ff00;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.container {
    width: 100%;
    max-width: 1200px;
    background: rgba(0, 0, 0, 0.8);
    border-radius: 10px;
    box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
    overflow: hidden;
}

.header {
    background: rgba(0, 255, 0, 0.1);
    padding: 20px;
    text-align: center;
    border-bottom: 2px solid #00ff00;
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
}

#terminal-container {
    padding: 20px;
    min-height: 500px;
    background: #000000;
}

.footer {
    background: rgba(0, 255, 0, 0.1);
    padding: 15px;
    text-align: center;
    border-top: 2px solid #00ff00;
    font-size: 0.9em;
    color: #00ff00;
    opacity: 0.7;
}

/* Terminal styling */
.xterm {
    padding: 10px;
}

.xterm-viewport {
    background-color: #000000 !important;
}

/* Responsive */
@media (max-width: 768px) {
    .header h1 {
        font-size: 1.5em;
    }
    
    #terminal-container {
        min-height: 400px;
        padding: 10px;
    }
}
"""
    
    # Create terminal.js with HTTP polling
    js_content = """// Terminal Trail - Browser Client with HTTP Polling
const term = new Terminal({
    cursorBlink: true,
    fontSize: 14,
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

// Session management
let sessionId = null;
let currentInput = '';
let isWaitingForInput = false;
let pollInterval = null;

async function startSession() {
    term.writeln('\\x1b[32mStarting Terminal Trail...\\x1b[0m');
    
    try {
        const response = await fetch('/api/session/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            throw new Error('Failed to start session');
        }
        
        const data = await response.json();
        sessionId = data.session_id;
        
        term.writeln('\\x1b[32m✓ Connected!\\x1b[0m\\r\\n');
        
        // Start polling for output
        startPolling();
        
    } catch (error) {
        term.writeln('\\x1b[31m✗ Connection error\\x1b[0m');
        term.writeln('\\x1b[31m' + error.message + '\\x1b[0m');
    }
}

function startPolling() {
    // Poll every 500ms for new output
    pollInterval = setInterval(async () => {
        if (!sessionId) return;
        
        try {
            const response = await fetch(`/api/session/${sessionId}/output`);
            
            if (!response.ok) {
                if (response.status === 404) {
                    term.writeln('\\r\\n\\x1b[31m✗ Session expired\\x1b[0m');
                    stopPolling();
                }
                return;
            }
            
            const data = await response.json();
            
            if (data.output) {
                term.write(data.output);
            }
            
            if (!data.running) {
                term.writeln('\\r\\n\\x1b[33mGame session ended\\x1b[0m');
                stopPolling();
            }
            
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 500);
}

function stopPolling() {
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
}

async function sendInput(input) {
    if (!sessionId) return;
    
    try {
        await fetch(`/api/session/${sessionId}/input`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: input })
        });
    } catch (error) {
        term.writeln('\\r\\n\\x1b[31m✗ Error sending input\\x1b[0m');
        console.error('Input error:', error);
    }
}

// Handle keyboard input
term.onData(data => {
    // Handle special keys
    if (data === '\\r') {  // Enter key
        term.write('\\r\\n');
        sendInput(currentInput);
        currentInput = '';
    } else if (data === '\\x7F') {  // Backspace
        if (currentInput.length > 0) {
            currentInput = currentInput.slice(0, -1);
            term.write('\\b \\b');
        }
    } else if (data === '\\x03') {  // Ctrl+C
        term.write('^C\\r\\n');
        currentInput = '';
    } else if (data.charCodeAt(0) < 32) {
        // Ignore other control characters
        return;
    } else {
        currentInput += data;
        term.write(data);
    }
});

// Handle paste
term.onPaste(data => {
    currentInput += data;
    term.write(data);
});

// Start the session when page loads
window.addEventListener('load', () => {
    startSession();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    stopPolling();
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
        logger.info("🎮 Terminal Trail Web Server Starting (HTTP Polling)")
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
