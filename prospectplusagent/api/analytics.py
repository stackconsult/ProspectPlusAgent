"""Analytics API endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime, timedelta

from prospectplusagent.models import AnalyticsResponse
from prospectplusagent.models.database import ProspectDB
from prospectplusagent.core.database import get_db

router = APIRouter()


@router.get("/overview", response_model=AnalyticsResponse)
async def get_analytics_overview(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get analytics overview."""
    query = db.query(ProspectDB)
    
    # Apply date filters
    if start_date:
        query = query.filter(ProspectDB.created_at >= start_date)
    if end_date:
        query = query.filter(ProspectDB.created_at <= end_date)
    
    # Total prospects
    total = query.count()
    
    # By status
    status_counts = {}
    for status_value in ["new", "contacted", "qualified", "proposal", "negotiation", "closed_won", "closed_lost"]:
        count = query.filter(ProspectDB.status == status_value).count()
        status_counts[status_value] = count
    
    # By priority
    priority_counts = {}
    for priority_value in ["low", "medium", "high", "critical"]:
        count = query.filter(ProspectDB.priority == priority_value).count()
        priority_counts[priority_value] = count
    
    # Conversion rate
    total_closed = status_counts.get("closed_won", 0) + status_counts.get("closed_lost", 0)
    conversion_rate = 0.0
    if total_closed > 0:
        conversion_rate = status_counts.get("closed_won", 0) / total_closed
    
    # Average score
    avg_score_result = query.filter(ProspectDB.score.isnot(None)).with_entities(
        func.avg(ProspectDB.score)
    ).scalar()
    avg_score = float(avg_score_result) if avg_score_result else None
    
    return {
        "total_prospects": total,
        "by_status": status_counts,
        "by_priority": priority_counts,
        "conversion_rate": conversion_rate,
        "avg_score": avg_score,
        "trends": None
    }


@router.get("/trends")
async def get_trends(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get prospect trends over time."""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get prospects created in the period
    prospects = db.query(ProspectDB).filter(
        ProspectDB.created_at >= start_date,
        ProspectDB.created_at <= end_date
    ).all()
    
    # Group by day
    daily_counts = {}
    for prospect in prospects:
        date_key = prospect.created_at.date().isoformat()
        daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
    
    return {
        "period": f"last_{days}_days",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily_counts": daily_counts,
        "total": len(prospects)
    }


@router.get("/top-industries")
async def get_top_industries(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get top industries by prospect count."""
    results = db.query(
        ProspectDB.industry,
        func.count(ProspectDB.id).label("count")
    ).filter(
        ProspectDB.industry.isnot(None)
    ).group_by(
        ProspectDB.industry
    ).order_by(
        func.count(ProspectDB.id).desc()
    ).limit(limit).all()
    
    return {
        "industries": [
            {"name": industry, "count": count}
            for industry, count in results
        ]
    }
