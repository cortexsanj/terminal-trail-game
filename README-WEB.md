# Terminal Trail - Web Version

Run Terminal Trail in your browser with a real terminal interface!

## 🚀 Quick Start (Local)

### 1. Install Dependencies

```bash
pip install -r requirements-web.txt
```

### 2. Run the Server

```bash
python3 web_server.py
```

The server will automatically create the static files if they don't exist.

### 3. Open in Browser

Navigate to: **http://localhost:8000**

You'll see a terminal interface where you can play Terminal Trail!

## 📦 What's Included

### New Files Created:
- `web_server.py` - FastAPI server with WebSocket support
- `requirements-web.txt` - Python dependencies for web version
- `Dockerfile` - Container configuration for deployment
- `web_static/` - HTML, CSS, JS files (auto-generated)
  - `index.html` - Main game page
  - `terminal.css` - Terminal styling
  - `terminal.js` - WebSocket client and terminal logic

### How It Works:
```
Browser (Xterm.js)
    ↓ WebSocket
FastAPI Server (web_server.py)
    ↓
Game Engine (your existing code)
    ↓
Virtual File System
```

## 🏃 Running Locally

### Option 1: Python Directly
```bash
python3 web_server.py
```

### Option 2: With Docker
```bash
# Build image
docker build -t terminal-quest .

# Run container
docker run -p 8000:8000 terminal-quest

# Open http://localhost:8000
```

### Option 3: With Uvicorn (Development)
```bash
uvicorn web_server:app --reload --host 0.0.0.0 --port 8000
```

## ☁️ Deploying to AWS App Runner

### Prerequisites:
1. AWS Account
2. AWS CLI installed and configured
3. Docker installed (optional, App Runner can build for you)

### Method 1: Deploy from GitHub (Easiest)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add web version"
   git push origin main
   ```

2. **Create App Runner Service**
   - Go to AWS Console → App Runner
   - Click "Create service"
   - Source: "Source code repository"
   - Connect your GitHub repo
   - Build settings:
     - Runtime: Python 3
     - Build command: `pip install -r requirements-web.txt`
     - Start command: `python3 web_server.py`
   - Or use Dockerfile (automatic detection)
   - Click "Create & Deploy"

3. **Done!** 
   - App Runner gives you a URL: `https://xxxxx.us-east-1.awsapprunner.com`
   - Your game is live!

### Method 2: Deploy from ECR (Container Registry)

1. **Build and push Docker image**
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
   
   # Create repository
   aws ecr create-repository --repository-name terminal-quest
   
   # Build image
   docker build -t terminal-quest .
   
   # Tag image
   docker tag terminal-quest:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/terminal-quest:latest
   
   # Push image
   docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/terminal-quest:latest
   ```

2. **Create App Runner service from ECR**
   - Go to AWS Console → App Runner
   - Click "Create service"
   - Source: "Container registry"
   - Select your ECR image
   - Port: 8000
   - Click "Create & Deploy"

### Method 3: Using AWS CLI

```bash
# Create apprunner.yaml configuration
cat > apprunner.yaml << EOF
version: 1.0
runtime: python3
build:
  commands:
    build:
      - pip install -r requirements-web.txt
run:
  command: python3 web_server.py
  network:
    port: 8000
EOF

# Deploy (requires AWS CLI v2)
aws apprunner create-service \
  --service-name terminal-quest \
  --source-configuration file://apprunner-source.json
```

## 🔧 Configuration

### Environment Variables

You can set these in App Runner or locally:

```bash
# Local
export PORT=8000
export DEBUG=false

# In App Runner Console
# Configuration → Environment variables
PORT=8000
DEBUG=false
```

### Custom Domain

1. Go to App Runner service
2. Click "Custom domains"
3. Add your domain (e.g., `play.terminalquest.com`)
4. Update DNS with provided CNAME

## 📊 Monitoring

### Local Development
- Server logs: Check terminal output
- Access logs: Uvicorn shows all requests

### AWS App Runner
- **Logs**: CloudWatch Logs (automatic)
- **Metrics**: CloudWatch Metrics (automatic)
  - Request count
  - Response time
  - Error rate
  - CPU/Memory usage
- **Health checks**: `/health` endpoint

## 💰 Cost Estimate (AWS App Runner)

### Free Tier (First 3 months):
- Build: 100 build minutes/month
- Compute: 2,000 vCPU minutes/month
- Memory: 4,000 GB minutes/month

### After Free Tier:
- **Small app** (0.25 vCPU, 0.5 GB): ~$5-10/month
- **Medium app** (1 vCPU, 2 GB): ~$20-30/month
- Only pay for what you use!

### Cost Breakdown:
- Provisioned: $0.007/hour (~$5/month for always-on)
- Active: $0.064/vCPU-hour + $0.007/GB-hour
- Requests: Free!

## 🐛 Troubleshooting

### Local Issues

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
# Or use different port
python3 web_server.py --port 8080
```

**Static files not found:**
```bash
python3 web_server.py --setup
```

**WebSocket connection fails:**
- Check firewall settings
- Ensure port 8000 is accessible
- Try http://127.0.0.1:8000 instead of localhost

### AWS App Runner Issues

**Build fails:**
- Check `requirements-web.txt` is in root
- Verify Python version (3.11)
- Check build logs in CloudWatch

**Service unhealthy:**
- Check `/health` endpoint returns 200
- Verify port 8000 is exposed
- Check application logs

**WebSocket doesn't work:**
- App Runner supports WebSockets by default
- Ensure using `wss://` (not `ws://`) in production
- Check browser console for errors

## 🔄 Updates

### Update Local Version:
```bash
git pull
pip install -r requirements-web.txt
python3 web_server.py
```

### Update AWS App Runner:
- **From GitHub**: Push to main branch (auto-deploys)
- **From ECR**: Push new image, trigger deployment
- **Manual**: Redeploy in App Runner console

## 📝 Next Steps

### Current Status:
- ✅ Web server running
- ✅ Terminal interface working
- ✅ WebSocket communication
- ⏳ Full game integration (in progress)

### To Complete:
1. Integrate full game engine with async I/O
2. Add user authentication (optional)
3. Add progress persistence (database)
4. Add multiplayer features (optional)

### Future Enhancements:
- User accounts and progress tracking
- Leaderboards
- Multiplayer mode
- Custom themes
- Mobile optimization
- Social sharing

## 🤝 Contributing

The web version is designed to be deployment-ready while keeping the core game logic unchanged. The same Python files work for both CLI and web versions!

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Xterm.js Documentation](https://xtermjs.org/)
- [AWS App Runner Documentation](https://docs.aws.amazon.com/apprunner/)
- [WebSocket Protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

## 🎮 Play Now!

**Local**: http://localhost:8000
**Production**: (Your App Runner URL here)

Enjoy learning Linux commands through an epic adventure! 🚀
