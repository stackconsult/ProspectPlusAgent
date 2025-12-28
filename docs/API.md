# API Documentation

## Overview

ProspectPlusAgent provides a comprehensive RESTful API for managing prospects, getting analytics, and interacting with the AI agent.

Base URL: `http://localhost:8080/api` (development)
Production URL: `https://prospectpulse-agent-739953812004.us-west1.run.app/api`

## Authentication

Most endpoints require JWT authentication. Obtain a token:

```bash
POST /api/auth/token
Content-Type: application/x-www-form-urlencoded

username=demo&password=demo123
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

Use the token in subsequent requests:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Endpoints

### Health & Info

#### GET /health
Check server health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

#### GET /api/info
Get API information.

**Response:**
```json
{
  "name": "ProspectPlusAgent",
  "version": "1.0.0",
  "environment": "production",
  "endpoints": { ... }
}
```

### Prospects

#### POST /api/prospects/
Create a new prospect.

**Request Body:**
```json
{
  "company_name": "Acme Corp",
  "contact_name": "John Doe",
  "email": "john@acme.com",
  "phone": "555-0100",
  "industry": "Technology",
  "company_size": "50-100",
  "website": "https://acme.com",
  "status": "new",
  "priority": "high",
  "notes": "Interested in our enterprise plan",
  "tags": ["enterprise", "saas"]
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "company_name": "Acme Corp",
  "contact_name": "John Doe",
  "email": "john@acme.com",
  "score": 0.75,
  "created_at": "2024-01-15T10:30:00Z",
  ...
}
```

#### GET /api/prospects/
List all prospects with optional filtering.

**Query Parameters:**
- `skip` (integer): Number of records to skip (default: 0)
- `limit` (integer): Number of records to return (default: 100, max: 1000)
- `status` (string): Filter by status
- `priority` (string): Filter by priority
- `industry` (string): Filter by industry

**Example:**
```
GET /api/prospects/?status=qualified&priority=high&limit=20
```

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "company_name": "Acme Corp",
    "contact_name": "John Doe",
    ...
  },
  ...
]
```

#### GET /api/prospects/{prospect_id}
Get a specific prospect by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "company_name": "Acme Corp",
  ...
}
```

#### PUT /api/prospects/{prospect_id}
Update a prospect.

**Request Body:** (all fields optional)
```json
{
  "status": "qualified",
  "priority": "critical",
  "notes": "Ready for proposal"
}
```

**Response:** `200 OK`

#### DELETE /api/prospects/{prospect_id}
Delete a prospect.

**Response:** `204 No Content`

#### POST /api/prospects/{prospect_id}/analyze
Run AI analysis on a prospect.

**Response:** `200 OK`
```json
{
  "prospect_id": "550e8400-e29b-41d4-a716-446655440000",
  "analysis": {
    "score": 0.85,
    "insights": [
      "High-value enterprise prospect",
      "Strong engagement signals"
    ],
    "recommendations": [
      "Schedule executive demo",
      "Prepare custom proposal"
    ],
    "next_steps": [
      "Initial discovery call",
      "Technical requirements gathering"
    ],
    "confidence": 0.87
  }
}
```

### Analytics

#### GET /api/analytics/overview
Get analytics overview.

**Query Parameters:**
- `start_date` (ISO datetime): Start date for filtering
- `end_date` (ISO datetime): End date for filtering

**Response:** `200 OK`
```json
{
  "total_prospects": 150,
  "by_status": {
    "new": 45,
    "contacted": 30,
    "qualified": 25,
    "proposal": 15,
    "negotiation": 10,
    "closed_won": 20,
    "closed_lost": 5
  },
  "by_priority": {
    "low": 30,
    "medium": 70,
    "high": 40,
    "critical": 10
  },
  "conversion_rate": 0.8,
  "avg_score": 0.72
}
```

#### GET /api/analytics/trends
Get prospect trends over time.

**Query Parameters:**
- `days` (integer): Number of days to look back (default: 30, max: 365)

**Response:** `200 OK`
```json
{
  "period": "last_30_days",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-01-31T00:00:00Z",
  "daily_counts": {
    "2024-01-15": 5,
    "2024-01-16": 3,
    ...
  },
  "total": 87
}
```

#### GET /api/analytics/top-industries
Get top industries by prospect count.

**Query Parameters:**
- `limit` (integer): Number of industries to return (default: 10, max: 50)

**Response:** `200 OK`
```json
{
  "industries": [
    {"name": "Technology", "count": 45},
    {"name": "Healthcare", "count": 30},
    {"name": "Finance", "count": 25},
    ...
  ]
}
```

### AI Agent

#### POST /api/agent/chat
Chat with the AI agent.

**Request Body:**
```json
{
  "query": "What are my highest priority prospects?",
  "context": {
    "user_id": "123"
  },
  "stream": false
}
```

**Response:** `200 OK`
```json
{
  "response": "Based on your current pipeline, you have 10 high-priority prospects...",
  "confidence": 0.85,
  "sources": [],
  "metadata": {}
}
```

#### GET /api/agent/status
Get agent status and capabilities.

**Response:** `200 OK`
```json
{
  "status": "operational",
  "capabilities": [
    "prospect_analysis",
    "chat_interaction",
    "recommendations",
    "insights_generation"
  ],
  "ai_enabled": true,
  "version": "1.0.0"
}
```

## Status Codes

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `204 No Content` - Request succeeded with no response body
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting

Currently, there are no rate limits in place. For production deployments, consider implementing rate limiting based on your requirements.

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Data Models

### Prospect Statuses
- `new` - New prospect, not yet contacted
- `contacted` - Initial contact made
- `qualified` - Qualified as viable prospect
- `proposal` - Proposal sent
- `negotiation` - In negotiation phase
- `closed_won` - Deal won
- `closed_lost` - Deal lost

### Prospect Priorities
- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority
- `critical` - Critical/urgent priority
