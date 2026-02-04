#!/usr/bin/env python3
"""
GitHub Webhook Listener for Auto-Deployment
Listens for push events and automatically deploys to EC2
"""

from flask import Flask, request, jsonify
import subprocess
import hmac
import hashlib
import os

app = Flask(__name__)

# Configuration
REPO_PATH = "/usr/share/nginx/html/terminal-trail-game"
SECRET_TOKEN = "your-secret-token-here"  # Change this!
BRANCH = "main"

def verify_signature(payload, signature):
    """Verify GitHub webhook signature"""
    if not signature:
        return False
    
    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False
    
    mac = hmac.new(
        SECRET_TOKEN.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    )
    
    return hmac.compare_digest(mac.hexdigest(), signature)

def deploy():
    """Deploy the application"""
    try:
        # Change to repo directory
        os.chdir(REPO_PATH)
        
        # Pull latest changes
        print("📥 Pulling latest changes...")
        subprocess.run(['git', 'pull', 'origin', BRANCH], check=True)
        
        # Regenerate static files
        print("🔧 Regenerating static files...")
        subprocess.run(['python3', 'web_server.py', '--setup'], check=True)
        
        # Restart application
        print("🔄 Restarting application...")
        subprocess.run(['pkill', '-f', 'python3 web_server.py'], check=False)
        subprocess.Popen(
            ['nohup', 'python3', 'web_server.py'],
            stdout=open('/tmp/terminal-trail.log', 'w'),
            stderr=subprocess.STDOUT,
            preexec_fn=os.setpgrp
        )
        
        print("✅ Deployment successful!")
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle GitHub webhook"""
    
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Parse payload
    payload = request.json
    
    # Check if it's a push event to the main branch
    if payload.get('ref') == f'refs/heads/{BRANCH}':
        print(f"🚀 Push detected to {BRANCH} branch")
        
        # Deploy
        if deploy():
            return jsonify({'status': 'success', 'message': 'Deployed successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Deployment failed'}), 500
    
    return jsonify({'status': 'ignored', 'message': 'Not a push to main branch'}), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    print("🎣 GitHub Webhook Listener Starting...")
    print(f"📁 Repo path: {REPO_PATH}")
    print(f"🌿 Branch: {BRANCH}")
    print("🔒 Remember to set SECRET_TOKEN!")
    app.run(host='0.0.0.0', port=9000)
