"""Data models for ProspectPlusAgent."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ProspectStatus(str, Enum):
    """Prospect status enumeration."""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class ProspectPriority(str, Enum):
    """Prospect priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProspectBase(BaseModel):
    """Base prospect model."""
    company_name: str = Field(..., min_length=1, max_length=200)
    contact_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    website: Optional[str] = None
    status: ProspectStatus = ProspectStatus.NEW
    priority: ProspectPriority = ProspectPriority.MEDIUM
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ProspectCreate(ProspectBase):
    """Model for creating a prospect."""
    pass


class ProspectUpdate(BaseModel):
    """Model for updating a prospect."""
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    website: Optional[str] = None
    status: Optional[ProspectStatus] = None
    priority: Optional[ProspectPriority] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class Prospect(ProspectBase):
    """Full prospect model with metadata."""
    id: str
    created_at: datetime
    updated_at: datetime
    last_contact: Optional[datetime] = None
    score: Optional[float] = None
    
    class Config:
        from_attributes = True


class AgentQuery(BaseModel):
    """Model for agent queries."""
    query: str = Field(..., min_length=1, max_length=2000)
    context: Optional[Dict[str, Any]] = None
    stream: bool = False


class AgentResponse(BaseModel):
    """Model for agent responses."""
    response: str
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None


class AnalyticsRequest(BaseModel):
    """Model for analytics requests."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    group_by: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


class AnalyticsResponse(BaseModel):
    """Model for analytics responses."""
    total_prospects: int
    by_status: Dict[str, int]
    by_priority: Dict[str, int]
    conversion_rate: float
    avg_score: Optional[float] = None
    trends: Optional[Dict[str, Any]] = None


class Token(BaseModel):
    """Authentication token model."""
    access_token: str
    token_type: str = "bearer"


class User(BaseModel):
    """User model."""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False


class UserInDB(User):
    """User model with hashed password."""
    hashed_password: str
