"""AI Agent service for prospect analysis and interaction."""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from prospectplusagent.config import settings

logger = logging.getLogger(__name__)


class ProspectAgent:
    """AI Agent for prospect analysis and management."""
    
    def __init__(self):
        """Initialize the agent."""
        self.client = None
        if OPENAI_AVAILABLE and settings.openai_api_key:
            try:
                self.client = OpenAI(api_key=settings.openai_api_key)
                logger.info("OpenAI client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
    
    async def analyze_prospect(
        self,
        prospect_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze a prospect and provide insights."""
        try:
            # Build context from prospect data
            context = self._build_prospect_context(prospect_data)
            
            # Generate analysis
            if self.client:
                response = await self._generate_openai_analysis(context)
            else:
                response = self._generate_fallback_analysis(prospect_data)
            
            return {
                "score": response.get("score", 0.5),
                "insights": response.get("insights", []),
                "recommendations": response.get("recommendations", []),
                "next_steps": response.get("next_steps", []),
                "confidence": response.get("confidence", 0.7)
            }
        except Exception as e:
            logger.error(f"Error analyzing prospect: {e}")
            return self._generate_fallback_analysis(prospect_data)
    
    async def chat(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a chat query about prospects."""
        try:
            if self.client:
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant specialized in prospect and lead management. "
                            "Help users analyze prospects, suggest next steps, and provide insights."
                        )
                    },
                    {"role": "user", "content": query}
                ]
                
                if context:
                    messages.insert(1, {
                        "role": "system",
                        "content": f"Context: {context}"
                    })
                
                response = self.client.chat.completions.create(
                    model=settings.default_model,
                    messages=messages,
                    temperature=settings.temperature,
                    max_tokens=settings.max_tokens
                )
                
                return {
                    "response": response.choices[0].message.content,
                    "confidence": 0.85,
                    "sources": []
                }
            else:
                return self._generate_fallback_chat_response(query)
                
        except Exception as e:
            logger.error(f"Error processing chat query: {e}")
            return self._generate_fallback_chat_response(query)
    
    def _build_prospect_context(self, prospect_data: Dict[str, Any]) -> str:
        """Build context string from prospect data."""
        parts = [
            f"Company: {prospect_data.get('company_name', 'Unknown')}",
            f"Contact: {prospect_data.get('contact_name', 'Unknown')}",
            f"Industry: {prospect_data.get('industry', 'Unknown')}",
            f"Status: {prospect_data.get('status', 'new')}",
            f"Priority: {prospect_data.get('priority', 'medium')}"
        ]
        if prospect_data.get('notes'):
            parts.append(f"Notes: {prospect_data['notes']}")
        return " | ".join(parts)
    
    async def _generate_openai_analysis(
        self,
        context: str
    ) -> Dict[str, Any]:
        """Generate analysis using OpenAI."""
        try:
            prompt = f"""Analyze this prospect and provide:
1. A score from 0-1 indicating quality
2. Key insights
3. Recommendations for engagement
4. Suggested next steps

Prospect: {context}

Provide a structured response."""

            response = self.client.chat.completions.create(
                model=settings.default_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a prospect analysis expert."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Parse response (simplified)
            return {
                "score": 0.75,
                "insights": [content[:200]],
                "recommendations": ["Follow up within 48 hours"],
                "next_steps": ["Schedule discovery call"],
                "confidence": 0.85
            }
        except Exception as e:
            logger.error(f"OpenAI analysis error: {e}")
            raise
    
    def _generate_fallback_analysis(
        self,
        prospect_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate basic analysis without AI."""
        # Simple rule-based scoring
        score = 0.5
        insights = []
        recommendations = []
        
        # Adjust score based on available data
        if prospect_data.get('industry'):
            score += 0.1
            insights.append(f"Industry: {prospect_data['industry']}")
        
        if prospect_data.get('company_size'):
            score += 0.1
        
        if prospect_data.get('website'):
            score += 0.1
            insights.append("Has company website")
        
        # Priority-based recommendations
        priority = prospect_data.get('priority', 'medium')
        if priority == 'high' or priority == 'critical':
            recommendations.append("High priority - immediate follow-up recommended")
        else:
            recommendations.append("Schedule follow-up within 1 week")
        
        return {
            "score": min(score, 1.0),
            "insights": insights or ["New prospect - needs initial qualification"],
            "recommendations": recommendations,
            "next_steps": ["Initial outreach", "Gather qualification data"],
            "confidence": 0.6
        }
    
    def _generate_fallback_chat_response(
        self,
        query: str
    ) -> Dict[str, Any]:
        """Generate fallback response when AI is unavailable."""
        return {
            "response": (
                "I'm currently running in limited mode. "
                "To enable full AI capabilities, please configure your OpenAI API key. "
                f"Your query was: {query}"
            ),
            "confidence": 0.5,
            "sources": []
        }


# Global agent instance
agent = ProspectAgent()
