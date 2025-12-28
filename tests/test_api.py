"""Tests for ProspectPlusAgent."""

import pytest
from fastapi.testclient import TestClient
from prospectplusagent.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_api_info_endpoint():
    """Test the API info endpoint."""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data


def test_root_endpoint():
    """Test the root endpoint returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


class TestProspects:
    """Test prospect endpoints."""
    
    def test_create_prospect(self):
        """Test creating a new prospect."""
        prospect_data = {
            "company_name": "Test Corp",
            "contact_name": "John Doe",
            "email": "john@testcorp.com",
            "phone": "555-0100",
            "industry": "Technology",
            "status": "new",
            "priority": "medium",
            "tags": []
        }
        
        response = client.post("/api/prospects/", json=prospect_data)
        assert response.status_code == 201
        data = response.json()
        assert data["company_name"] == "Test Corp"
        assert data["contact_name"] == "John Doe"
        assert "id" in data
        
        # Clean up
        prospect_id = data["id"]
        client.delete(f"/api/prospects/{prospect_id}")
    
    def test_list_prospects(self):
        """Test listing prospects."""
        response = client.get("/api/prospects/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_duplicate_email(self):
        """Test that duplicate emails are rejected."""
        prospect_data = {
            "company_name": "Test Corp",
            "contact_name": "John Doe",
            "email": "duplicate@test.com",
            "status": "new",
            "priority": "medium",
            "tags": []
        }
        
        # Create first prospect
        response1 = client.post("/api/prospects/", json=prospect_data)
        assert response1.status_code == 201
        prospect_id = response1.json()["id"]
        
        # Try to create duplicate
        response2 = client.post("/api/prospects/", json=prospect_data)
        assert response2.status_code == 400
        
        # Clean up
        client.delete(f"/api/prospects/{prospect_id}")


class TestAnalytics:
    """Test analytics endpoints."""
    
    def test_analytics_overview(self):
        """Test analytics overview endpoint."""
        response = client.get("/api/analytics/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total_prospects" in data
        assert "by_status" in data
        assert "by_priority" in data
        assert "conversion_rate" in data
    
    def test_trends_endpoint(self):
        """Test trends endpoint."""
        response = client.get("/api/analytics/trends?days=7")
        assert response.status_code == 200
        data = response.json()
        assert "period" in data
        assert "daily_counts" in data


class TestAgent:
    """Test agent endpoints."""
    
    def test_agent_status(self):
        """Test agent status endpoint."""
        response = client.get("/api/agent/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
        assert "capabilities" in data
        assert "ai_enabled" in data
    
    def test_agent_chat(self):
        """Test agent chat endpoint."""
        query_data = {
            "query": "What is a prospect?",
            "stream": False
        }
        
        response = client.post("/api/agent/chat", json=query_data)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "confidence" in data
