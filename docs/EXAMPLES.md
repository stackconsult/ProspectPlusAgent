# ProspectPlusAgent - Quick Start Examples

## Web UI Usage

### 1. Starting the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
prospectplus init

# Start the server
prospectplus serve

# Open browser to http://localhost:8080
```

### 2. Using the Dashboard

The dashboard shows:
- Total prospects count
- Qualified prospects
- High priority prospects
- Conversion rate
- Recent prospects list

### 3. Managing Prospects

**Add a New Prospect:**
1. Click "Add Prospect" button
2. Fill in the form:
   - Company Name (required)
   - Contact Name (required)
   - Email (required)
   - Phone, Industry, Website (optional)
   - Status and Priority
3. Click "Add Prospect"
4. AI automatically analyzes and scores the prospect

**View and Filter Prospects:**
- Use status filter (New, Contacted, Qualified, etc.)
- Use priority filter (Low, Medium, High, Critical)
- View prospect details, scores, and information

### 4. AI Agent Chat

Navigate to the "AI Agent" tab:
- Ask questions about prospects
- Get recommendations
- Analyze prospect quality
- Request next steps

**Example queries:**
- "What are my highest priority prospects?"
- "Show me prospects in the technology industry"
- "Which prospects should I contact first?"
- "Analyze my pipeline"

### 5. Analytics

View analytics dashboard:
- Prospects by status (chart)
- Prospects by priority (chart)
- Top industries
- Conversion rates
- Trends over time

## CLI Usage

### Server Management

```bash
# Start server
prospectplus serve --host 0.0.0.0 --port 8080

# Check server status
prospectplus status

# Initialize database
prospectplus init
```

### Prospect Management

```bash
# List all prospects
prospectplus prospect list

# List with filters
prospectplus prospect list --status qualified --priority high

# Add a prospect
prospectplus prospect add \
  --company "TechCorp" \
  --contact "Jane Doe" \
  --email "jane@techcorp.com" \
  --industry "SaaS" \
  --priority high

# Add with full details
prospectplus prospect add \
  --company "Innovation Labs" \
  --contact "John Smith" \
  --email "john@innovationlabs.com" \
  --phone "555-0123" \
  --industry "Technology" \
  --status contacted \
  --priority medium \
  --notes "Interested in enterprise plan"
```

### AI Agent Interaction

```bash
# Chat with AI agent
prospectplus chat "What are my top prospects?"

prospectplus chat "Analyze prospects in the technology sector"

prospectplus chat "Give me recommendations for follow-up"
```

### Analytics

```bash
# View analytics
prospectplus analytics
```

## API Usage

### Using cURL

**Get Health Status:**
```bash
curl http://localhost:8080/health
```

**Create a Prospect:**
```bash
curl -X POST http://localhost:8080/api/prospects/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "contact_name": "John Doe",
    "email": "john@acme.com",
    "industry": "Technology",
    "status": "new",
    "priority": "high",
    "tags": []
  }'
```

**List Prospects:**
```bash
# All prospects
curl http://localhost:8080/api/prospects/

# With filters
curl "http://localhost:8080/api/prospects/?status=qualified&priority=high"
```

**Get Analytics:**
```bash
curl http://localhost:8080/api/analytics/overview
```

**Chat with AI:**
```bash
curl -X POST http://localhost:8080/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are my highest priority prospects?"
  }'
```

### Using Python

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Create a prospect
        prospect_data = {
            "company_name": "TechStart Inc",
            "contact_name": "Jane Smith",
            "email": "jane@techstart.com",
            "industry": "SaaS",
            "status": "new",
            "priority": "high",
            "tags": []
        }
        
        response = await client.post(
            "http://localhost:8080/api/prospects/",
            json=prospect_data
        )
        prospect = response.json()
        print(f"Created prospect: {prospect['id']}")
        print(f"AI Score: {prospect['score']}")
        
        # List all prospects
        response = await client.get("http://localhost:8080/api/prospects/")
        prospects = response.json()
        print(f"\nTotal prospects: {len(prospects)}")
        
        # Get analytics
        response = await client.get("http://localhost:8080/api/analytics/overview")
        analytics = response.json()
        print(f"\nAnalytics:")
        print(f"  Total: {analytics['total_prospects']}")
        print(f"  By Status: {analytics['by_status']}")
        print(f"  Conversion Rate: {analytics['conversion_rate']*100:.1f}%")
        
        # Chat with AI
        response = await client.post(
            "http://localhost:8080/api/agent/chat",
            json={"query": "Analyze my high-priority prospects"}
        )
        chat_response = response.json()
        print(f"\nAI Response: {chat_response['response']}")

asyncio.run(main())
```

### Using JavaScript/TypeScript

```javascript
// Create a prospect
async function createProspect() {
    const response = await fetch('http://localhost:8080/api/prospects/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            company_name: 'Global Solutions',
            contact_name: 'Sarah Johnson',
            email: 'sarah@globalsolutions.com',
            industry: 'Consulting',
            status: 'new',
            priority: 'high',
            tags: []
        })
    });
    
    const prospect = await response.json();
    console.log('Created:', prospect);
    return prospect;
}

// List prospects
async function listProspects(status = null, priority = null) {
    let url = 'http://localhost:8080/api/prospects/';
    const params = new URLSearchParams();
    
    if (status) params.append('status', status);
    if (priority) params.append('priority', priority);
    
    if (params.toString()) url += `?${params.toString()}`;
    
    const response = await fetch(url);
    const prospects = await response.json();
    console.log(`Found ${prospects.length} prospects`);
    return prospects;
}

// Get analytics
async function getAnalytics() {
    const response = await fetch('http://localhost:8080/api/analytics/overview');
    const analytics = await response.json();
    console.log('Analytics:', analytics);
    return analytics;
}

// Chat with AI
async function chatWithAI(query) {
    const response = await fetch('http://localhost:8080/api/agent/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query })
    });
    
    const result = await response.json();
    console.log('AI:', result.response);
    return result;
}

// Example usage
(async () => {
    await createProspect();
    const prospects = await listProspects('qualified', 'high');
    const analytics = await getAnalytics();
    await chatWithAI('What are my top prospects?');
})();
```

## Docker Deployment

### Build and Run Locally

```bash
# Build Docker image
docker build -t prospectplusagent .

# Run container
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your-key \
  -e SECRET_KEY=your-secret \
  prospectplusagent

# Run with environment file
docker run -p 8080:8080 --env-file .env prospectplusagent
```

## Google Cloud Run Deployment

### Quick Deploy

```bash
# Make script executable
chmod +x deploy.sh

# Deploy (replace with your project ID)
./deploy.sh your-project-id us-west1
```

### Manual Deploy

```bash
# Set project
gcloud config set project YOUR-PROJECT-ID

# Build and push
docker build -t gcr.io/YOUR-PROJECT-ID/prospectplusagent .
docker push gcr.io/YOUR-PROJECT-ID/prospectplusagent

# Deploy to Cloud Run
gcloud run deploy prospectpulse-agent \
  --image gcr.io/YOUR-PROJECT-ID/prospectplusagent \
  --platform managed \
  --region us-west1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --set-env-vars "OPENAI_API_KEY=your-key,SECRET_KEY=your-secret"
```

## Environment Variables

Create a `.env` file:

```env
# App Configuration
APP_NAME=ProspectPlusAgent
ENVIRONMENT=production
PORT=8080

# API Keys
OPENAI_API_KEY=sk-...your-key...
ANTHROPIC_API_KEY=sk-ant-...your-key...

# Security
SECRET_KEY=your-super-secret-jwt-key-change-this

# Database (optional, defaults to SQLite)
DATABASE_URL=postgresql://user:pass@localhost/prospectplus
```

## Common Tasks

### Reset Database

```bash
# Delete database file
rm prospectplus.db

# Reinitialize
prospectplus init
```

### View Logs

```bash
# Server logs are in ./logs/
tail -f logs/app.log
```

### Export Data

```bash
# Using API
curl http://localhost:8080/api/prospects/ > prospects.json

# View analytics
curl http://localhost:8080/api/analytics/overview | jq
```

## Troubleshooting

### Server won't start

```bash
# Check if port is in use
lsof -i :8080

# Try different port
prospectplus serve --port 8081
```

### Database errors

```bash
# Reinitialize database
prospectplus init
```

### AI features not working

```bash
# Check agent status
curl http://localhost:8080/api/agent/status

# Verify API key is set
echo $OPENAI_API_KEY
```

## Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Configure production database (PostgreSQL)
- [ ] Set up proper CORS origins
- [ ] Enable HTTPS
- [ ] Set up monitoring and logging
- [ ] Configure backups
- [ ] Set environment to "production"
- [ ] Review and set resource limits
- [ ] Configure secrets in Cloud Secret Manager
- [ ] Set up CI/CD pipeline

## Support

For issues or questions:
1. Check the [README.md](../README.md)
2. Review [API Documentation](API.md)
3. See [Deployment Guide](DEPLOYMENT.md)
4. Open an issue on GitHub
