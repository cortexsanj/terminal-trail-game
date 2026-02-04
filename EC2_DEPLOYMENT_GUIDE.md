# Terminal Trail - EC2 Deployment Guide

## Why EC2?

✅ **Simplest** - Just a Linux server, no containers needed
✅ **Cheapest** - t3.micro free tier or ~$8/month
✅ **WebSocket Support** - Full support, no special config
✅ **Direct GitHub Deploy** - Pull and run, that's it!
✅ **Full Control** - SSH access, easy debugging

## Cost Comparison

| Service | Monthly Cost | Complexity | WebSocket |
|---------|-------------|------------|-----------|
| **EC2 t3.micro** | **$8-10** | Low | ✅ Yes |
| App Runner | $5-10 | Low | ❌ No |
| ECS Fargate | $25-35 | Medium | ✅ Yes |

**Winner for your use case: EC2!**

## Quick Start (5 Minutes)

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. **Name**: `terminal-trail`
3. **AMI**: Amazon Linux 2023 (Free tier eligible) - Recommended for AWS
   - Alternative: Amazon Linux 2 (older but stable)
   - Alternative: Ubuntu Server 22.04 LTS
4. **Instance type**: `t3.micro` (1 vCPU, 1 GB RAM) - Free tier!
   - Alternative: `t2.micro` (older generation, also free tier)
5. **Key pair**: Create new or use existing (for SSH access)
6. **Network settings**:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere (0.0.0.0/0)
   - Allow HTTPS (port 443) from anywhere (0.0.0.0/0)
   - Allow Custom TCP (port 8000) from anywhere (for testing)
7. **Storage**: 8 GB (default, free tier)
8. Click **Launch Instance**

### Step 2: Connect to Your Instance

```bash
# For Amazon Linux 2/2023 (default user is 'ec2-user')
ssh -i your-key.pem ec2-user@YOUR_EC2_PUBLIC_IP

# For Ubuntu (default user is 'ubuntu')
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 3: Install Dependencies

#### For Amazon Linux 2023 (Recommended):

```bash
# Update system
sudo dnf update -y

# Install Python 3.11 (comes with AL2023)
sudo dnf install -y python3.11 python3.11-pip git

# Install nginx (for reverse proxy)
sudo dnf install -y nginx

# Install certbot (for SSL - optional)
sudo dnf install -y python3-certbot-nginx

# Start and enable nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### For Amazon Linux 2 (Older):

```bash
# Update system
sudo yum update -y

# Install Python 3.11 from amazon-linux-extras
sudo amazon-linux-extras install python3.11 -y

# Install git
sudo yum install -y git

# Install nginx
sudo amazon-linux-extras install nginx1 -y

# Install certbot
sudo yum install -y certbot python3-certbot-nginx

# Start and enable nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### For Ubuntu 22.04:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip git

# Install nginx (for reverse proxy)
sudo apt install -y nginx

# Install certbot (for SSL - optional)
sudo apt install -y certbot python3-certbot-nginx
```

### Step 4: Clone Your Repository

```bash
# Clone your repo (use ec2-user for Amazon Linux, ubuntu for Ubuntu)
cd /home/ec2-user  # For Amazon Linux
# OR
cd /home/ubuntu    # For Ubuntu

git clone https://github.com/cortexsanj/terminal-trail-game.git
cd terminal-trail-game

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-web.txt
```

### Step 5: Test the Application

```bash
# Run the server
python3 web_server.py
```

Open browser: `http://YOUR_EC2_PUBLIC_IP:8000`

If it works, press Ctrl+C to stop.

### Step 6: Set Up as a Service (Auto-start)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/terminal-trail.service
```

Paste this content (adjust User and paths for your OS):

#### For Amazon Linux (ec2-user):

```ini
[Unit]
Description=Terminal Trail Web Server
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/terminal-trail-game
Environment="PATH=/home/ec2-user/terminal-trail-game/venv/bin"
ExecStart=/home/ec2-user/terminal-trail-game/venv/bin/python3 web_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### For Ubuntu:

```ini
[Unit]
Description=Terminal Trail Web Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/terminal-trail-game
Environment="PATH=/home/ubuntu/terminal-trail-game/venv/bin"
ExecStart=/home/ubuntu/terminal-trail-game/venv/bin/python3 web_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and exit (Ctrl+X, Y, Enter).

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable terminal-trail

# Start service
sudo systemctl start terminal-trail

# Check status
sudo systemctl status terminal-trail
```

### Step 7: Set Up Nginx Reverse Proxy

This allows you to use port 80 (HTTP) instead of 8000:

```bash
sudo nano /etc/nginx/sites-available/terminal-trail
```

Paste this content:

```nginx
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_IP;  # Or your domain name

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_read_timeout 86400;
    }
}
```

Enable the site:

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/terminal-trail /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

Now access your app at: `http://YOUR_EC2_PUBLIC_IP`

### Step 8: (Optional) Add SSL Certificate

If you have a domain name:

```bash
# Point your domain to EC2 IP in DNS
# Then run:
sudo certbot --nginx -d yourdomain.com

# Follow prompts, certbot will auto-configure nginx for HTTPS
```

## Updating Your App

### Manual Update:

```bash
# SSH into EC2
# For Amazon Linux:
ssh -i your-key.pem ec2-user@YOUR_EC2_PUBLIC_IP
# For Ubuntu:
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Navigate to app directory
cd /home/ec2-user/terminal-trail-game  # Amazon Linux
# OR
cd /home/ubuntu/terminal-trail-game    # Ubuntu

# Pull latest changes
git pull origin main

# Restart service
sudo systemctl restart terminal-trail
```

### Auto-Update Script:

Create an update script:

#### For Amazon Linux:

```bash
nano /home/ec2-user/update-terminal-trail.sh
```

Paste:

```bash
#!/bin/bash
cd /home/ec2-user/terminal-trail-game
git pull origin main
source venv/bin/activate
pip install -r requirements-web.txt
sudo systemctl restart terminal-trail
echo "✅ Terminal Trail updated!"
```

Make executable:

```bash
chmod +x /home/ec2-user/update-terminal-trail.sh
```

#### For Ubuntu:

```bash
nano /home/ubuntu/update-terminal-trail.sh
```

Paste:

```bash
#!/bin/bash
cd /home/ubuntu/terminal-trail-game
git pull origin main
source venv/bin/activate
pip install -r requirements-web.txt
sudo systemctl restart terminal-trail
echo "✅ Terminal Trail updated!"
```

Make executable:

```bash
chmod +x /home/ubuntu/update-terminal-trail.sh
```

Now you can update with:

```bash
./update-terminal-trail.sh
```

### GitHub Webhook Auto-Deploy (Advanced):

Set up a webhook endpoint that pulls and restarts on push to GitHub.

## Monitoring

### View Logs:

```bash
# Service logs
sudo journalctl -u terminal-trail -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Check Service Status:

```bash
sudo systemctl status terminal-trail
```

### Restart Service:

```bash
sudo systemctl restart terminal-trail
```

## Security Best Practices

### 1. Update Security Group

Only allow necessary ports:
- SSH (22) - Only from your IP
- HTTP (80) - From anywhere
- HTTPS (443) - From anywhere
- Remove port 8000 (use nginx proxy instead)

### 2. Set Up Firewall

#### For Amazon Linux:

```bash
# Amazon Linux uses firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Allow necessary ports
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

#### For Ubuntu:

```bash
# Enable UFW firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 3. Keep System Updated

#### For Amazon Linux:

```bash
# Set up automatic security updates
sudo dnf install -y dnf-automatic
sudo systemctl enable --now dnf-automatic.timer
```

#### For Ubuntu:

```bash
# Set up automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 4. Create Backups

```bash
# Backup script (adjust path for your OS)
sudo crontab -e

# For Amazon Linux - Add this line (daily backup at 2 AM):
0 2 * * * tar -czf /home/ec2-user/backup-$(date +\%Y\%m\%d).tar.gz /home/ec2-user/terminal-trail-game

# For Ubuntu - Add this line (daily backup at 2 AM):
0 2 * * * tar -czf /home/ubuntu/backup-$(date +\%Y\%m\%d).tar.gz /home/ubuntu/terminal-trail-game
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u terminal-trail -n 50

# Check if port 8000 is in use
sudo lsof -i :8000
# OR on Amazon Linux:
sudo ss -tulpn | grep 8000

# Test manually (adjust path for your OS)
cd /home/ec2-user/terminal-trail-game  # Amazon Linux
# OR
cd /home/ubuntu/terminal-trail-game    # Ubuntu

source venv/bin/activate
python3 web_server.py
```

### WebSocket Connection Fails

```bash
# Check nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# Check firewall
# For Amazon Linux:
sudo firewall-cmd --list-all
# For Ubuntu:
sudo ufw status
```

### Can't Connect to EC2

- Check security group allows your IP on port 22
- Verify key pair permissions: `chmod 400 your-key.pem`
- Check instance is running in EC2 console

## Cost Breakdown

### t3.micro Instance:
- **Free Tier**: 750 hours/month for 12 months (FREE!)
- **After Free Tier**: ~$0.0104/hour = ~$7.60/month

### Data Transfer:
- First 1 GB/month: FREE
- Next 10 TB: $0.09/GB

### Storage (8 GB EBS):
- First 30 GB: FREE (free tier)
- After: $0.10/GB/month

**Total: FREE for 12 months, then ~$8-10/month**

## Scaling Options

### Vertical Scaling (Bigger Instance):
```bash
# Stop instance
# Change instance type in console
# Start instance
```

Instance types:
- t3.micro: 1 vCPU, 1 GB RAM (~$8/month)
- t3.small: 2 vCPU, 2 GB RAM (~$15/month)
- t3.medium: 2 vCPU, 4 GB RAM (~$30/month)

### Horizontal Scaling (Multiple Instances):
- Add Application Load Balancer
- Launch multiple EC2 instances
- Similar to ECS but manual management

## Advantages of EC2

✅ **Simple** - No containers, no orchestration
✅ **Cheap** - Free tier or ~$8/month
✅ **Full Control** - SSH access, install anything
✅ **Easy Updates** - Just `git pull` and restart
✅ **WebSocket Works** - No special configuration
✅ **Easy Debugging** - Direct access to logs and files

## Disadvantages of EC2

❌ **Manual Management** - You handle updates, security
❌ **Single Point of Failure** - If instance dies, app is down
❌ **No Auto-Scaling** - Manual scaling only
❌ **You Manage OS** - Security patches, updates

## When to Use What?

| Use Case | Recommendation |
|----------|---------------|
| **Learning/Testing** | EC2 t3.micro |
| **Small Production (<100 users)** | EC2 t3.small |
| **Medium Production (100-1000 users)** | ECS Fargate |
| **Large Production (1000+ users)** | ECS Fargate + Auto-scaling |
| **No WebSocket needed** | App Runner |

## Quick Commands Reference

### For Amazon Linux:

```bash
# Start service
sudo systemctl start terminal-trail

# Stop service
sudo systemctl stop terminal-trail

# Restart service
sudo systemctl restart terminal-trail

# View logs
sudo journalctl -u terminal-trail -f

# Update app
cd /home/ec2-user/terminal-trail-game && git pull && sudo systemctl restart terminal-trail

# Check nginx
sudo nginx -t
sudo systemctl restart nginx

# View nginx logs
sudo tail -f /var/log/nginx/access.log

# Check firewall
sudo firewall-cmd --list-all
```

### For Ubuntu:

```bash
# Start service
sudo systemctl start terminal-trail

# Stop service
sudo systemctl stop terminal-trail

# Restart service
sudo systemctl restart terminal-trail

# View logs
sudo journalctl -u terminal-trail -f

# Update app
cd /home/ubuntu/terminal-trail-game && git pull && sudo systemctl restart terminal-trail

# Check nginx
sudo nginx -t
sudo systemctl restart nginx

# View nginx logs
sudo tail -f /var/log/nginx/access.log

# Check firewall
sudo ufw status
```

## Next Steps

1. ✅ Launch EC2 instance (t3.micro)
2. ✅ SSH and install dependencies
3. ✅ Clone repo and test
4. ✅ Set up systemd service
5. ✅ Configure nginx reverse proxy
6. 🎯 Optional: Add custom domain
7. 🎯 Optional: Add SSL with Let's Encrypt
8. 🎯 Optional: Set up monitoring (CloudWatch)

## Resources

- [EC2 Getting Started](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt SSL](https://letsencrypt.org/getting-started/)
- [Systemd Services](https://www.freedesktop.org/software/systemd/man/systemd.service.html)

---

**Recommendation: Start with EC2!** It's the simplest, cheapest, and most straightforward option for your use case. You can always migrate to ECS later if you need auto-scaling.
