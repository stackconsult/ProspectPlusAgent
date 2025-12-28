# Deployment Guide

## Overview

This guide covers deploying ProspectPlusAgent to various environments, with a focus on Google Cloud Run.

## Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed
- Docker installed
- Project created in GCP
- Billing enabled

## Google Cloud Run Deployment

### Step 1: Setup Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Build Docker Image

```bash
# Build the image
docker build -t gcr.io/YOUR-PROJECT-ID/prospectplusagent:latest .

# Test locally
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your-key \
  -e SECRET_KEY=your-secret \
  gcr.io/YOUR-PROJECT-ID/prospectplusagent:latest
```

### Step 3: Push to Container Registry

```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Push the image
docker push gcr.io/YOUR-PROJECT-ID/prospectplusagent:latest
```

### Step 4: Deploy to Cloud Run

```bash
# Deploy
gcloud run deploy prospectpulse-agent \
  --image gcr.io/YOUR-PROJECT-ID/prospectplusagent:latest \
  --platform managed \
  --region us-west1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --set-env-vars "OPENAI_API_KEY=your-key,SECRET_KEY=your-secret,ENVIRONMENT=production"
```

### Step 5: Configure Secrets (Recommended)

Instead of passing secrets as environment variables, use Secret Manager:

```bash
# Create secrets
echo -n "your-openai-key" | gcloud secrets create openai-api-key --data-file=-
echo -n "your-secret-key" | gcloud secrets create jwt-secret-key --data-file=-

# Deploy with secrets
gcloud run deploy prospectpulse-agent \
  --image gcr.io/YOUR-PROJECT-ID/prospectplusagent:latest \
  --platform managed \
  --region us-west1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --set-secrets "OPENAI_API_KEY=openai-api-key:latest,SECRET_KEY=jwt-secret-key:latest"
```

### Step 6: Setup Custom Domain (Optional)

```bash
# Map domain
gcloud run domain-mappings create \
  --service prospectpulse-agent \
  --domain your-domain.com \
  --region us-west1
```

### Using the Deploy Script

The repository includes a deployment script:

```bash
# Make it executable
chmod +x deploy.sh

# Run it
./deploy.sh YOUR-PROJECT-ID us-west1
```

## Production Database Setup

For production, use Cloud SQL PostgreSQL:

### Step 1: Create Cloud SQL Instance

```bash
gcloud sql instances create prospectplus-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-west1
```

### Step 2: Create Database

```bash
gcloud sql databases create prospectplus \
  --instance=prospectplus-db
```

### Step 3: Create User

```bash
gcloud sql users create prospectplus \
  --instance=prospectplus-db \
  --password=your-secure-password
```

### Step 4: Update Cloud Run Service

```bash
# Get the connection name
INSTANCE_CONNECTION_NAME=$(gcloud sql instances describe prospectplus-db \
  --format='value(connectionName)')

# Update deployment with Cloud SQL
gcloud run deploy prospectpulse-agent \
  --add-cloudsql-instances $INSTANCE_CONNECTION_NAME \
  --set-env-vars "DATABASE_URL=postgresql://prospectplus:your-password@/prospectplus?host=/cloudsql/$INSTANCE_CONNECTION_NAME"
```

## Environment Variables for Production

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes* |
| `SECRET_KEY` | JWT secret (use strong random string) | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Recommended |
| `ENVIRONMENT` | Set to "production" | Yes |
| `ALLOWED_ORIGINS` | CORS allowed origins | No |

*Or ANTHROPIC_API_KEY

## Monitoring and Logging

### View Logs

```bash
# Stream logs
gcloud run services logs tail prospectpulse-agent --region=us-west1

# View logs in console
gcloud run services logs read prospectpulse-agent --region=us-west1 --limit=50
```

### Setup Monitoring

1. Go to Cloud Console > Monitoring
2. Create dashboards for:
   - Request rate
   - Error rate
   - Response latency
   - Memory usage
   - CPU utilization

### Setup Alerts

```bash
# Example: Alert on high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Error Rate" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

## Scaling Configuration

### Auto-scaling

Cloud Run automatically scales based on traffic. Configure limits:

```bash
gcloud run services update prospectpulse-agent \
  --min-instances=1 \
  --max-instances=10 \
  --concurrency=80 \
  --cpu-throttling \
  --region=us-west1
```

### Resource Allocation

- **Memory**: 2Gi recommended (minimum 512Mi)
- **CPU**: 2 recommended (minimum 1)
- **Concurrency**: 80 requests per instance
- **Timeout**: 300 seconds default

## Backup and Recovery

### Database Backups

```bash
# Enable automated backups
gcloud sql instances patch prospectplus-db \
  --backup-start-time=03:00

# Manual backup
gcloud sql backups create \
  --instance=prospectplus-db
```

### Restore from Backup

```bash
# List backups
gcloud sql backups list --instance=prospectplus-db

# Restore
gcloud sql backups restore BACKUP_ID \
  --backup-instance=prospectplus-db \
  --backup-id=BACKUP_ID
```

## Security Best Practices

1. **Use Secret Manager** for sensitive data
2. **Enable VPC** for database access
3. **Set up IAM roles** properly
4. **Enable Cloud Armor** for DDoS protection
5. **Use HTTPS only** (enforced by Cloud Run)
6. **Rotate secrets** regularly
7. **Enable audit logging**
8. **Set up security scanning** for containers

## CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Cloud SDK
        uses: google-github-actions/setup-gcloud@v0
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
      
      - name: Build and Push
        run: |
          docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/prospectplusagent:${{ github.sha }} .
          docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/prospectplusagent:${{ github.sha }}
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy prospectpulse-agent \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/prospectplusagent:${{ github.sha }} \
            --platform managed \
            --region us-west1
```

## Cost Optimization

1. **Set max instances** to control costs
2. **Use minimum instances** carefully (always running = always charged)
3. **Optimize memory** allocation
4. **Use Cloud SQL proxy** for database connections
5. **Implement caching** where possible
6. **Monitor usage** regularly

## Troubleshooting

### Container doesn't start

- Check logs: `gcloud run services logs read prospectpulse-agent`
- Verify environment variables are set
- Test image locally first

### Database connection issues

- Verify Cloud SQL instance is running
- Check connection string format
- Ensure Cloud SQL Admin API is enabled
- Verify IAM permissions

### High latency

- Check if cold starts are the issue
- Consider increasing min-instances
- Optimize database queries
- Enable caching

### Out of memory

- Increase memory allocation
- Check for memory leaks
- Optimize data processing

## Health Checks

Cloud Run automatically health checks `/` endpoint. The app provides `/health`:

```json
GET /health
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

## Rollback

```bash
# List revisions
gcloud run revisions list --service=prospectpulse-agent --region=us-west1

# Rollback to previous revision
gcloud run services update-traffic prospectpulse-agent \
  --to-revisions=REVISION_NAME=100 \
  --region=us-west1
```
