"""Prospects API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from prospectplusagent.models import (
    Prospect,
    ProspectCreate,
    ProspectUpdate,
    ProspectStatus,
    ProspectPriority
)
from prospectplusagent.models.database import ProspectDB
from prospectplusagent.core.database import get_db
from prospectplusagent.core.agent import agent

router = APIRouter()


@router.post("/", response_model=Prospect, status_code=status.HTTP_201_CREATED)
async def create_prospect(
    prospect: ProspectCreate,
    db: Session = Depends(get_db)
):
    """Create a new prospect."""
    # Check if email already exists
    existing = db.query(ProspectDB).filter(ProspectDB.email == prospect.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A prospect with this email already exists"
        )
    
    # Create new prospect
    db_prospect = ProspectDB(
        id=str(uuid.uuid4()),
        **prospect.model_dump()
    )
    
    db.add(db_prospect)
    db.commit()
    db.refresh(db_prospect)
    
    # Analyze prospect with AI
    try:
        analysis = await agent.analyze_prospect(db_prospect.to_dict())
        db_prospect.score = analysis.get("score")
        db.commit()
        db.refresh(db_prospect)
    except Exception as e:
        # Continue even if analysis fails
        pass
    
    return db_prospect.to_dict()


@router.get("/", response_model=List[Prospect])
async def list_prospects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[ProspectStatus] = None,
    priority: Optional[ProspectPriority] = None,
    industry: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List prospects with optional filtering."""
    query = db.query(ProspectDB)
    
    if status:
        query = query.filter(ProspectDB.status == status.value)
    if priority:
        query = query.filter(ProspectDB.priority == priority.value)
    if industry:
        query = query.filter(ProspectDB.industry == industry)
    
    prospects = query.offset(skip).limit(limit).all()
    return [p.to_dict() for p in prospects]


@router.get("/{prospect_id}", response_model=Prospect)
async def get_prospect(
    prospect_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific prospect by ID."""
    prospect = db.query(ProspectDB).filter(ProspectDB.id == prospect_id).first()
    if not prospect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect not found"
        )
    return prospect.to_dict()


@router.put("/{prospect_id}", response_model=Prospect)
async def update_prospect(
    prospect_id: str,
    prospect_update: ProspectUpdate,
    db: Session = Depends(get_db)
):
    """Update a prospect."""
    prospect = db.query(ProspectDB).filter(ProspectDB.id == prospect_id).first()
    if not prospect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect not found"
        )
    
    # Update fields
    update_data = prospect_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prospect, field, value)
    
    prospect.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(prospect)
    
    return prospect.to_dict()


@router.delete("/{prospect_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prospect(
    prospect_id: str,
    db: Session = Depends(get_db)
):
    """Delete a prospect."""
    prospect = db.query(ProspectDB).filter(ProspectDB.id == prospect_id).first()
    if not prospect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect not found"
        )
    
    db.delete(prospect)
    db.commit()
    return None


@router.post("/{prospect_id}/analyze")
async def analyze_prospect_endpoint(
    prospect_id: str,
    db: Session = Depends(get_db)
):
    """Analyze a prospect using AI."""
    prospect = db.query(ProspectDB).filter(ProspectDB.id == prospect_id).first()
    if not prospect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect not found"
        )
    
    analysis = await agent.analyze_prospect(prospect.to_dict())
    
    # Update score
    prospect.score = analysis.get("score")
    db.commit()
    
    return {
        "prospect_id": prospect_id,
        "analysis": analysis
    }
