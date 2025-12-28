# ProspectPlusAgent 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)

**Enterprise-grade AI Agent for Prospect and Lead Management**

ProspectPlusAgent is a comprehensive, production-ready application that combines AI-powered prospect analysis with a modern web interface and command-line tools. Built for Google Cloud Run deployment, it provides enterprise-level capabilities for managing and analyzing business prospects.

## 🌟 Features

### Core Capabilities
- **🤖 AI-Powered Analysis**: Intelligent prospect scoring and insights using GPT-4/Claude
- **📊 Real-time Dashboard**: Beautiful, responsive web interface for prospect management
- **💬 Interactive AI Chat**: Natural language interaction with your prospect data
- **📈 Advanced Analytics**: Comprehensive reporting and trend analysis
- **🔒 Enterprise Security**: JWT authentication, password hashing, and secure API endpoints
- **⚡ High Performance**: FastAPI backend with async/await support
- **🎯 RESTful API**: Complete API with OpenAPI/Swagger documentation
- **🖥️ CLI Interface**: Full-featured command-line tools for automation
- **☁️ Cloud-Ready**: Optimized for Google Cloud Run deployment

### Technical Features
- **Modern Tech Stack**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic
- **AI Integration**: OpenAI GPT-4, Anthropic Claude support
- **Vector Database**: ChromaDB for semantic search
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Vanilla JavaScript with modern CSS
- **Containerized**: Docker support for easy deployment
- **Production-Ready**: Health checks, monitoring, logging

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip or poetry
- (Optional) Docker for containerized deployment
- (Optional) Google Cloud SDK for Cloud Run deployment

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/stackconsult/ProspectPlusAgent.git
   cd ProspectPlusAgent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or using poetry
   poetry install
   ```

3. **Initialize the application**
   ```bash
   # Using CLI
   prospectplus init
   
   # Or manually create .env from template
   cp .env.example .env
   ```

4. **Configure environment variables**
   Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   SECRET_KEY=your-secret-key-for-jwt
   ```

5. **Start the server**
   ```bash
   # Using CLI
   prospectplus serve
   
   # Or using uvicorn directly
   uvicorn prospectplusagent.main:app --reload
   ```

6. **Open your browser**
   Navigate to [http://localhost:8080](http://localhost:8080)

## 📖 Usage

### Web Interface

The web dashboard provides a complete interface for managing prospects:

1. **Dashboard**: View key metrics and recent prospects
2. **Prospects**: Add, view, and manage all your prospects
3. **AI Agent**: Chat with the AI for insights and recommendations
4. **Analytics**: View detailed analytics and trends

### Command-Line Interface

ProspectPlusAgent includes a powerful CLI:

```bash
# Initialize the application
prospectplus init

# Start the server
prospectplus serve --host 0.0.0.0 --port 8080

# Check server status
prospectplus status

# List prospects
prospectplus prospect list --limit 20

# Add a prospect
prospectplus prospect add \
  --company "Acme Corp" \
  --contact "John Doe" \
  --email "john@acme.com" \
  --industry "Technology" \
  --priority high

# Chat with AI agent
prospectplus chat "What are my highest priority prospects?"

# View analytics
prospectplus analytics
```

### API Documentation

Once the server is running, visit:
- **Swagger UI**: [http://localhost:8080/api/docs](http://localhost:8080/api/docs)
- **ReDoc**: [http://localhost:8080/api/redoc](http://localhost:8080/api/redoc)

#### Key API Endpoints

**Prospects**
- `POST /api/prospects/` - Create a new prospect
- `GET /api/prospects/` - List all prospects (with filters)
- `GET /api/prospects/{id}` - Get a specific prospect
- `PUT /api/prospects/{id}` - Update a prospect
- `DELETE /api/prospects/{id}` - Delete a prospect
- `POST /api/prospects/{id}/analyze` - AI analysis of a prospect

**Analytics**
- `GET /api/analytics/overview` - Get analytics overview
- `GET /api/analytics/trends` - Get trend data
- `GET /api/analytics/top-industries` - Get top industries

**AI Agent**
- `POST /api/agent/chat` - Chat with the AI agent
- `GET /api/agent/status` - Get agent status

**Authentication**
- `POST /api/auth/token` - Get access token
- `GET /api/auth/me` - Get current user info

### Example API Usage

```python
import httpx

# Create a prospect
async with httpx.AsyncClient() as client:
    prospect = {
        "company_name": "TechStart Inc",
        "contact_name": "Jane Smith",
        "email": "jane@techstart.com",
        "industry": "SaaS",
        "status": "new",
        "priority": "high"
    }
    response = await client.post(
        "http://localhost:8080/api/prospects/",
        json=prospect
    )
    new_prospect = response.json()
    print(f"Created prospect: {new_prospect['id']}")

# Chat with AI
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8080/api/agent/chat",
        json={"query": "Analyze my high-priority prospects"}
    )
    chat_response = response.json()
    print(chat_response['response'])
```

## 🐳 Docker Deployment

### Build and run with Docker

```bash
# Build the image
docker build -t prospectplusagent .

# Run the container
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your-key \
  -e SECRET_KEY=your-secret \
  prospectplusagent
```

## ☁️ Google Cloud Run Deployment

### Prerequisites
- Google Cloud account
- `gcloud` CLI installed and configured
- Container Registry API enabled

### Deploy to Cloud Run

```bash
# Make deploy script executable
chmod +x deploy.sh

# Deploy (replace with your project ID)
./deploy.sh your-project-id us-west1

# Or manually:
# Build and push
docker build -t gcr.io/YOUR-PROJECT-ID/prospectplusagent .
docker push gcr.io/YOUR-PROJECT-ID/prospectplusagent

# Deploy
gcloud run deploy prospectpulse-agent \
  --image gcr.io/YOUR-PROJECT-ID/prospectplusagent \
  --platform managed \
  --region us-west1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --set-env-vars OPENAI_API_KEY=your-key,SECRET_KEY=your-secret
```

### Environment Variables for Production

Set these in Cloud Run:
- `OPENAI_API_KEY` - Your OpenAI API key
- `ANTHROPIC_API_KEY` - Your Anthropic API key (optional)
- `SECRET_KEY` - JWT secret key (generate a secure random string)
- `DATABASE_URL` - PostgreSQL connection string (for production)
- `ENVIRONMENT` - Set to "production"

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=prospectplusagent

# Run specific test file
pytest tests/test_api.py
```

## 🏗️ Architecture

```
ProspectPlusAgent/
├── prospectplusagent/          # Main application package
│   ├── api/                    # API endpoints
│   │   ├── prospects.py        # Prospect management
│   │   ├── analytics.py        # Analytics endpoints
│   │   ├── agent.py            # AI agent endpoints
│   │   └── auth.py             # Authentication
│   ├── core/                   # Core services
│   │   ├── database.py         # Database connection
│   │   ├── agent.py            # AI agent service
│   │   └── auth.py             # Auth utilities
│   ├── models/                 # Data models
│   │   ├── __init__.py         # Pydantic models
│   │   └── database.py         # SQLAlchemy models
│   ├── static/                 # Static files
│   │   ├── css/                # Stylesheets
│   │   └── js/                 # JavaScript
│   ├── templates/              # HTML templates
│   ├── cli.py                  # CLI interface
│   ├── config.py               # Configuration
│   └── main.py                 # FastAPI application
├── tests/                      # Test suite
├── docs/                       # Documentation
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Poetry configuration
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | No* |
| `ANTHROPIC_API_KEY` | Anthropic API key | - | No |
| `SECRET_KEY` | JWT secret key | (insecure default) | Yes (production) |
| `DATABASE_URL` | Database connection string | `sqlite:///./prospectplus.db` | No |
| `ENVIRONMENT` | Environment (dev/production) | `production` | No |
| `PORT` | Server port | `8080` | No |
| `HOST` | Server host | `0.0.0.0` | No |
| `DEFAULT_MODEL` | AI model to use | `gpt-4-turbo-preview` | No |

*AI features work in limited mode without API keys

## 📊 Database Schema

### Prospects Table
- `id` (UUID) - Unique identifier
- `company_name` - Company name
- `contact_name` - Contact person name
- `email` - Email address (unique)
- `phone` - Phone number
- `industry` - Industry/sector
- `company_size` - Company size
- `website` - Company website
- `status` - Current status (new, contacted, qualified, etc.)
- `priority` - Priority level (low, medium, high, critical)
- `notes` - Free-form notes
- `tags` - JSON array of tags
- `score` - AI-generated quality score (0-1)
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp
- `last_contact` - Last contact timestamp

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- AI powered by [OpenAI](https://openai.com/) and [Anthropic](https://www.anthropic.com/)
- UI inspired by modern SaaS dashboards
- Deployed on [Google Cloud Run](https://cloud.google.com/run)

## 📧 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🗺️ Roadmap

- [ ] Email integration for automated outreach
- [ ] Calendar integration for scheduling
- [ ] Advanced reporting and export features
- [ ] Multi-user support with teams
- [ ] Webhooks for integrations
- [ ] Mobile app
- [ ] Enhanced AI models and fine-tuning

---

**Built with ❤️ by the StackConsult Team**