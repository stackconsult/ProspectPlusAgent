"""Database models using SQLAlchemy."""

from sqlalchemy import Column, String, DateTime, Float, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()


class ProspectDB(Base):
    """Database model for prospects."""
    
    __tablename__ = "prospects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_name = Column(String(200), nullable=False, index=True)
    contact_name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(50))
    industry = Column(String(100), index=True)
    company_size = Column(String(50))
    website = Column(String(255))
    status = Column(String(50), nullable=False, default="new", index=True)
    priority = Column(String(50), nullable=False, default="medium", index=True)
    notes = Column(String)
    tags = Column(JSON, default=list)
    score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    last_contact = Column(DateTime(timezone=True))
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "email": self.email,
            "phone": self.phone,
            "industry": self.industry,
            "company_size": self.company_size,
            "website": self.website,
            "status": self.status,
            "priority": self.priority,
            "notes": self.notes,
            "tags": self.tags or [],
            "score": self.score,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_contact": self.last_contact
        }


class InteractionDB(Base):
    """Database model for prospect interactions."""
    
    __tablename__ = "interactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prospect_id = Column(String, nullable=False, index=True)
    interaction_type = Column(String(50), nullable=False)
    content = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
