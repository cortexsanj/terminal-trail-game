# Terminal Trail - ECS Fargate Deployment Guide

## Why ECS Fargate?

✅ **WebSocket Support** - Full support with Application Load Balancer
✅ **Sticky Sessions** - ALB handles session affinity
✅ **Auto Scaling** - Scale based on traffic
✅ **More Control** - Full container orchestration

## Prerequisites

1. AWS Account
2. AWS CLI installed and configured
3. Docker installed locally
4. Your GitHub repo: https://github.com/cortexsanj/terminal-trail-game

## Deployment Options

### Option 1: Manual Deployment (Quick Start)

#### Step 1: Create ECR Repository

```bash
# Set your region
export AWS_REGION=eu-west-2
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create ECR repository
aws ecr create-repository \
    --repository-name terminal-trail \
    --region $AWS_REGION
```

#### Step 2: Build and Push Docker Image

```bash
# Login to ECR
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build image
docker build -t terminal-trail .

# Tag image
docker tag terminal-trail:latest \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/terminal-trail:latest

# Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/terminal-trail:latest
```

#### Step 3: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster \
    --cluster-name terminal-trail-cluster \
    --region $AWS_REGION
```

#### Step 4: Create Task Definition

```bash
# Update ecs-task-definition.json with your account ID and region
# Then register it:
aws ecs register-task-definition \
    --cli-input-json file://ecs-task-definition.json \
    --region $AWS_REGION
```

#### Step 5: Create Application Load Balancer (via Console)

1. Go to EC2 → Load Balancers → Create Load Balancer
2. Choose "Application Load Balancer"
3. Name: `terminal-trail-alb`
4. Scheme: Internet-facing
5. Listeners: HTTP (80) and HTTPS (443) if you have SSL
6. Select your VPC and at least 2 subnets
7. Create security group:
   - Allow inbound: 80 (HTTP), 443 (HTTPS)
   - Allow outbound: All
8. Create target group:
   - Name: `terminal-trail-tg`
   - Target type: IP
   - Protocol: HTTP
   - Port: 8000
   - Health check path: `/health`
   - **Enable sticky sessions** (important for WebSocket!)
     - Stickiness type: Load balancer generated cookie
     - Duration: 1 day (86400 seconds)

#### Step 6: Create ECS Service

```bash
# Create service (replace with your subnet IDs and security group)
aws ecs create-service \
    --cluster terminal-trail-cluster \
    --service-name terminal-trail-service \
    --task-definition terminal-trail \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:REGION:ACCOUNT:targetgroup/terminal-trail-tg/xxx,containerName=terminal-trail,containerPort=8000" \
    --region $AWS_REGION
```

### Option 2: GitHub Actions Auto-Deploy (Recommended)

This automatically builds and deploys when you push to GitHub!

#### Step 1: Create GitHub Secrets

Go to your repo → Settings → Secrets and variables → Actions

Add these secrets:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `AWS_REGION` - e.g., `eu-west-2`
- `AWS_ACCOUNT_ID` - Your AWS account ID

#### Step 2: Create GitHub Actions Workflow

I'll create this file for you: `.github/workflows/deploy-ecs.yml`

#### Step 3: Push to GitHub

```bash
git add .
git commit -m "Add ECS deployment"
git push origin main
```

GitHub Actions will automatically:
1. Build Docker image
2. Push to ECR
3. Update ECS service
4. Deploy new version

## Configuration Files

### Files You Have (Ready for ECS):
- ✅ `Dockerfile` - Container definition
- ✅ `requirements-web.txt` - Python dependencies
- ✅ `web_server.py` - WebSocket-enabled server

### Files Created for ECS:
- 🆕 `ecs-task-definition.json` - ECS task configuration
- 🆕 `ECS_DEPLOYMENT_GUIDE.md` - This guide
- 🆕 `.github/workflows/deploy-ecs.yml` - Auto-deployment (optional)

### Files NOT Used by ECS:
- ❌ `apprunner.yaml` - App Runner specific (ignore for ECS)

## Important: ALB Configuration for WebSocket

**Critical settings for WebSocket support:**

1. **Target Group Settings:**
   - Stickiness: **ENABLED** (load balancer generated cookie)
   - Stickiness duration: 86400 seconds (1 day)
   - Deregistration delay: 30 seconds

2. **Security Group:**
   - Inbound: Allow 80, 443 from 0.0.0.0/0
   - Outbound: Allow all

3. **Health Check:**
   - Path: `/health`
   - Healthy threshold: 2
   - Unhealthy threshold: 3
   - Timeout: 5 seconds
   - Interval: 30 seconds

## Cost Estimate

### ECS Fargate Pricing (eu-west-2):
- **vCPU**: $0.04048 per vCPU per hour
- **Memory**: $0.004445 per GB per hour

### Example Configuration (0.25 vCPU, 0.5 GB):
- vCPU cost: 0.25 × $0.04048 × 730 hours = ~$7.39/month
- Memory cost: 0.5 × $0.004445 × 730 hours = ~$1.62/month
- **Total**: ~$9/month

### Additional Costs:
- **ALB**: ~$16/month (fixed) + $0.008 per LCU-hour
- **Data Transfer**: First 1 GB free, then $0.09/GB
- **CloudWatch Logs**: ~$0.50/GB ingested

**Total estimated cost: $25-35/month** for a small app

Compare to App Runner: $5-10/month (but no WebSocket support)

## Accessing Your App

Once deployed, your app will be available at:
- **ALB DNS**: `terminal-trail-alb-xxxxx.eu-west-2.elb.amazonaws.com`
- **Custom Domain**: Configure Route 53 to point to ALB

## Monitoring

### CloudWatch Logs
```bash
# View logs
aws logs tail /ecs/terminal-trail --follow --region $AWS_REGION
```

### ECS Service Status
```bash
# Check service
aws ecs describe-services \
    --cluster terminal-trail-cluster \
    --services terminal-trail-service \
    --region $AWS_REGION
```

## Updating Your App

### Manual Update:
```bash
# Build and push new image
docker build -t terminal-trail .
docker tag terminal-trail:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/terminal-trail:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/terminal-trail:latest

# Force new deployment
aws ecs update-service \
    --cluster terminal-trail-cluster \
    --service terminal-trail-service \
    --force-new-deployment \
    --region $AWS_REGION
```

### With GitHub Actions:
Just push to main branch - automatic deployment!

## Troubleshooting

### Service Won't Start
- Check CloudWatch logs: `/ecs/terminal-trail`
- Verify security groups allow traffic
- Check task definition has correct image URI

### WebSocket Connection Fails
- Verify ALB has sticky sessions enabled
- Check security group allows inbound 80/443
- Ensure health check passes at `/health`

### High Costs
- Reduce task count (desired count)
- Use smaller CPU/memory (0.25 vCPU, 0.5 GB minimum)
- Set up auto-scaling based on traffic

## Scaling

### Manual Scaling:
```bash
aws ecs update-service \
    --cluster terminal-trail-cluster \
    --service terminal-trail-service \
    --desired-count 2 \
    --region $AWS_REGION
```

### Auto Scaling:
Configure in ECS console:
- Target tracking: CPU utilization 70%
- Min tasks: 1
- Max tasks: 10

## Next Steps

1. ✅ Test locally: `docker build -t terminal-trail . && docker run -p 8000:8000 terminal-trail`
2. ✅ Create ECR repository
3. ✅ Push image to ECR
4. ✅ Create ECS cluster and task definition
5. ✅ Create ALB with sticky sessions
6. ✅ Create ECS service
7. ✅ Test WebSocket connection
8. 🎯 Optional: Set up GitHub Actions for auto-deploy
9. 🎯 Optional: Add custom domain with Route 53

## Resources

- [ECS Fargate Documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)
- [ALB WebSocket Support](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html)
- [ECS Task Definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [GitHub Actions for ECS](https://github.com/aws-actions/amazon-ecs-deploy-task-definition)
