# AWS App Runner Deployment Checklist

## ✅ Pre-Deployment Verification

### Required Files (All Present ✓)
- [x] `Dockerfile` - Container configuration
- [x] `requirements-web.txt` - Python dependencies
- [x] `web_server.py` - FastAPI application
- [x] `game_engine.py` - Game logic
- [x] `file_system.py` - Virtual file system
- [x] `terminal_handler.py` - Command processor
- [x] `story_manager.py` - Story content
- [x] `progress_tracker.py` - Save/load
- [x] `challenges/*.json` - All 63 challenges
- [x] `assets/story_files/*` - Story content
- [x] `.gitignore` - Excludes venv, web_static, etc.

### Configuration Verified ✓
- [x] Port 8000 (App Runner default)
- [x] Host 0.0.0.0 (binds to all interfaces)
- [x] Health check endpoint `/health`
- [x] WebSocket support (built-in)
- [x] Auto-generates web_static/ on startup
- [x] No hardcoded localhost references

## 🚀 Deployment Steps

### Option 1: Deploy from GitHub (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Terminal Trail"
   git remote add origin https://github.com/YOUR_USERNAME/terminal-trail.git
   git push -u origin main
   ```

2. **Create App Runner Service**
   - Go to AWS Console → App Runner
   - Click "Create service"
   - **Source**: Repository
   - **Repository type**: GitHub
   - Connect your GitHub account
   - Select repository: `terminal-trail`
   - Branch: `main`
   - **Deployment settings**:
     - Source directory: `/` (root)
     - Deployment trigger: Automatic (on push)
   
3. **Configure Build**
   - **Configuration source**: Use a configuration file
   - App Runner will auto-detect `Dockerfile`
   - Or manually specify:
     - **Build command**: (leave empty, Dockerfile handles it)
     - **Start command**: (leave empty, Dockerfile CMD handles it)
     - **Port**: 8000

4. **Configure Service**
   - **Service name**: `terminal-trail`
   - **vCPU**: 0.25 or 1 (start small)
   - **Memory**: 0.5 GB or 2 GB
   - **Environment variables**: None needed
   - **Auto scaling**: 
     - Min: 1
     - Max: 3 (or more if needed)

5. **Deploy**
   - Click "Create & Deploy"
   - Wait 5-10 minutes for first deployment
   - App Runner will:
     - Clone your repo
     - Build Docker image
     - Deploy container
     - Provide HTTPS URL

6. **Access Your Game**
   - URL format: `https://xxxxx.us-east-1.awsapprunner.com`
   - Open in browser
   - Terminal Trail will load automatically!

### Option 2: Deploy from ECR (Container Registry)

1. **Build and Push Image**
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin \
     YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
   
   # Create repository
   aws ecr create-repository --repository-name terminal-trail
   
   # Build image
   docker build -t terminal-trail .
   
   # Tag image
   docker tag terminal-trail:latest \
     YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/terminal-trail:latest
   
   # Push image
   docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/terminal-trail:latest
   ```

2. **Create App Runner Service from ECR**
   - Go to AWS Console → App Runner
   - Click "Create service"
   - **Source**: Container registry
   - **Provider**: Amazon ECR
   - Select your image
   - **Port**: 8000
   - Click "Create & Deploy"

## 🧪 Testing Deployment

### 1. Health Check
```bash
curl https://YOUR_APP_URL.awsapprunner.com/health
# Should return: {"status":"healthy","service":"terminal-trail"}
```

### 2. Web Interface
- Open `https://YOUR_APP_URL.awsapprunner.com` in browser
- Should see Terminal Trail interface
- Terminal should connect via WebSocket
- Game should start automatically

### 3. Game Functionality
- Type `ls` - should list files
- Type `help` - should show commands
- Play through Challenge 1
- Progress should save

## 📊 Monitoring

### CloudWatch Logs
- Automatic logging enabled
- View at: CloudWatch → Log groups → `/aws/apprunner/terminal-trail/...`
- Check for:
  - Application startup logs
  - WebSocket connections
  - Command execution
  - Errors

### CloudWatch Metrics
- Request count
- Response time (latency)
- Active instances
- CPU/Memory usage
- 4xx/5xx errors

### App Runner Dashboard
- Service status
- Deployment history
- Logs (last 100 lines)
- Metrics overview

## 💰 Cost Estimate

### Free Tier (First 3 months)
- 100 build minutes/month
- 2,000 vCPU minutes/month
- 4,000 GB minutes/month

### After Free Tier
**Small Configuration (0.25 vCPU, 0.5 GB)**
- Provisioned: ~$5/month (always-on)
- Active: ~$0.064/vCPU-hour + $0.007/GB-hour
- **Total**: ~$5-10/month for hobby use

**Medium Configuration (1 vCPU, 2 GB)**
- Provisioned: ~$20/month
- Active: Higher during traffic
- **Total**: ~$20-30/month

## 🔧 Troubleshooting

### Build Fails
- Check `requirements-web.txt` exists
- Verify Python version (3.11)
- Check Dockerfile syntax
- View build logs in App Runner console

### Service Unhealthy
- Check `/health` endpoint returns 200
- Verify port 8000 is exposed
- Check application logs for errors
- Ensure `web_server.py` starts correctly

### WebSocket Connection Fails
- App Runner supports WebSockets by default
- Check browser console for errors
- Verify using `wss://` (not `ws://`) in production
- Check CORS settings if needed

### Game Doesn't Load
- Check static files are generated (auto-created on startup)
- Verify all game files copied to container
- Check challenges/ and assets/ directories exist
- View application logs

## 🔄 Updates & Redeployment

### Automatic (GitHub)
- Push to main branch
- App Runner auto-detects and redeploys
- Zero downtime deployment

### Manual
- App Runner console → "Deploy"
- Or push new image to ECR

### Rollback
- App Runner console → Deployments
- Select previous deployment
- Click "Rollback"

## 🌐 Custom Domain (Optional)

1. **Add Custom Domain**
   - App Runner console → Custom domains
   - Add domain: `play.terminaltrail.com`
   - App Runner provides validation records

2. **Update DNS**
   - Add CNAME record in your DNS provider
   - Point to App Runner domain
   - Wait for validation (5-30 minutes)

3. **SSL Certificate**
   - Automatic via AWS Certificate Manager
   - Free and auto-renewing

## ✅ Final Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] Repository is public or App Runner has access
- [ ] Dockerfile is in root directory
- [ ] requirements-web.txt is in root directory
- [ ] All game files committed
- [ ] .gitignore excludes venv/ and web_static/
- [ ] Tested locally with Docker (optional)

After deploying:
- [ ] Service shows "Running" status
- [ ] Health check passes
- [ ] Can access web interface
- [ ] Terminal connects via WebSocket
- [ ] Game plays correctly
- [ ] Progress saves/loads

## 🎉 Success!

Your Terminal Trail game is now live on AWS App Runner!

**Share your URL**: `https://xxxxx.us-east-1.awsapprunner.com`

Players can now learn Linux commands through your browser-based adventure! 🚀
