# GitHub Webhook Auto-Deployment Setup

Automatically deploy to EC2 when you push to GitHub!

## How It Works

```
You push to GitHub
    ↓
GitHub sends webhook to EC2
    ↓
EC2 receives webhook
    ↓
Runs: git pull → regenerate files → restart app
    ↓
✅ Deployed!
```

## Setup (10 minutes)

### Step 1: Copy Webhook Script to EC2

From your local machine:

```bash
# Copy the webhook script
scp -i your-key.pem deploy-webhook.py ec2-user@35.179.169.43:/home/ec2-user/
```

Or create it directly on EC2:

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@35.179.169.43

# Create the file
nano ~/deploy-webhook.py
# Paste the content from deploy-webhook.py
```

### Step 2: Install Flask on EC2

```bash
# Install Flask
pip3 install flask

# Or use system package
sudo dnf install -y python3-flask  # Amazon Linux
```

### Step 3: Generate Secret Token

```bash
# Generate a random secret token
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output (e.g., `a1b2c3d4e5f6...`)

### Step 4: Update Webhook Script

```bash
nano ~/deploy-webhook.py
```

Change this line:
```python
SECRET_TOKEN = "your-secret-token-here"  # Change this!
```

To:
```python
SECRET_TOKEN = "a1b2c3d4e5f6..."  # Your generated token
```

Save and exit.

### Step 5: Update Security Group

In AWS Console:
1. Go to EC2 → Security Groups
2. Find your instance's security group
3. Add inbound rule:
   - Type: Custom TCP
   - Port: 9000
   - Source: 0.0.0.0/0 (or GitHub's IP ranges for better security)

### Step 6: Start Webhook Listener

```bash
# Test it first
python3 ~/deploy-webhook.py

# You should see:
# 🎣 GitHub Webhook Listener Starting...
# 📁 Repo path: /usr/share/nginx/html/terminal-trail-game
# 🌿 Branch: main
```

Press Ctrl+C to stop.

### Step 7: Run as Service (Auto-start)

Create systemd service:

```bash
sudo nano /etc/systemd/system/github-webhook.service
```

Paste:

```ini
[Unit]
Description=GitHub Webhook Listener
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user
ExecStart=/usr/bin/python3 /home/ec2-user/deploy-webhook.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable github-webhook
sudo systemctl start github-webhook
sudo systemctl status github-webhook
```

### Step 8: Configure GitHub Webhook

1. Go to your GitHub repo: https://github.com/cortexsanj/terminal-trail-game
2. Click **Settings** → **Webhooks** → **Add webhook**
3. Fill in:
   - **Payload URL**: `http://35.179.169.43:9000/webhook`
   - **Content type**: `application/json`
   - **Secret**: Your secret token from Step 3
   - **Which events**: Just the push event
   - **Active**: ✅ Checked
4. Click **Add webhook**

### Step 9: Test It!

On your local machine:

```bash
# Make a small change
echo "# Test" >> README.md

# Commit and push
git add README.md
git commit -m "Test webhook deployment"
git push origin main
```

Watch the webhook logs on EC2:

```bash
sudo journalctl -u github-webhook -f
```

You should see:
```
🚀 Push detected to main branch
📥 Pulling latest changes...
🔧 Regenerating static files...
🔄 Restarting application...
✅ Deployment successful!
```

Check your site: http://35.179.169.43 - it should be updated!

## Troubleshooting

### Webhook Not Triggering

Check GitHub webhook delivery:
1. Go to repo → Settings → Webhooks
2. Click on your webhook
3. Check "Recent Deliveries"
4. Look for errors

### Check Webhook Logs

```bash
# View webhook service logs
sudo journalctl -u github-webhook -f

# Check if webhook is running
sudo systemctl status github-webhook

# Check if port 9000 is listening
sudo ss -tulpn | grep 9000
```

### Signature Verification Failed

Make sure the secret token in:
- `deploy-webhook.py` (on EC2)
- GitHub webhook settings

Are **exactly the same**.

### Deployment Fails

Check permissions:

```bash
# Make sure ec2-user can access the repo
ls -la /usr/share/nginx/html/terminal-trail-game

# Make sure ec2-user can kill/start processes
ps aux | grep web_server
```

## Security Best Practices

### 1. Use GitHub IP Ranges (Recommended)

Instead of allowing 0.0.0.0/0 on port 9000, restrict to GitHub's IPs:

Get GitHub's webhook IPs:
```bash
curl https://api.github.com/meta | jq .hooks
```

Add only those IPs to your security group.

### 2. Use HTTPS (Advanced)

Set up SSL for the webhook endpoint:
- Get SSL certificate (Let's Encrypt)
- Configure nginx to proxy to webhook
- Use `https://yourdomain.com/webhook` instead

### 3. Rotate Secret Token

Change the secret token periodically:
```bash
# Generate new token
python3 -c "import secrets; print(secrets.token_hex(32))"

# Update deploy-webhook.py
nano ~/deploy-webhook.py

# Update GitHub webhook settings

# Restart service
sudo systemctl restart github-webhook
```

## Alternative: Simple Cron Job

If webhooks are too complex, use a cron job to check for updates every 5 minutes:

```bash
# Edit crontab
crontab -e

# Add this line (checks every 5 minutes)
*/5 * * * * cd /usr/share/nginx/html/terminal-trail-game && git fetch && [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ] && /home/ec2-user/update.sh
```

This checks if there are new commits and runs the update script if needed.

## Comparison

| Method | Speed | Complexity | Reliability |
|--------|-------|------------|-------------|
| **Manual SSH** | Instant | Simple | 100% |
| **Webhook** | Instant | Medium | 95% |
| **Cron Job** | 5 min delay | Simple | 90% |

## Recommendation

**Start with manual SSH + update script** (Option 1 from previous answer).

**Add webhook later** when you're deploying frequently and want automation.

## Quick Commands

```bash
# View webhook logs
sudo journalctl -u github-webhook -f

# Restart webhook
sudo systemctl restart github-webhook

# Stop webhook
sudo systemctl stop github-webhook

# Manual deploy (if webhook fails)
~/update.sh
```

## Files Created

- `deploy-webhook.py` - Webhook listener script
- `WEBHOOK_SETUP_GUIDE.md` - This guide
- `/etc/systemd/system/github-webhook.service` - Systemd service

---

**Bottom Line:** Webhooks are cool but manual deployment with `update.sh` is simpler and more reliable for small projects. Use webhooks when you're deploying multiple times per day!
