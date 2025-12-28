"""Agent API endpoints."""

from fastapi import APIRouter, HTTPException, status
from typing import Optional

from prospectplusagent.models import AgentQuery, AgentResponse
from prospectplusagent.core.agent import agent

router = APIRouter()


@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(query: AgentQuery):
    """Chat with the AI agent."""
    try:
        response = await agent.chat(
            query=query.query,
            context=query.context
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/status")
async def get_agent_status():
    """Get agent status and capabilities."""
    return {
        "status": "operational",
        "capabilities": [
            "prospect_analysis",
            "chat_interaction",
            "recommendations",
            "insights_generation"
        ],
        "ai_enabled": agent.client is not None,
        "version": "1.0.0"
    }
