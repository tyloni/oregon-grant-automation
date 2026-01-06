from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.database import get_db
from app.models.grant import Grant
from app.schemas.grant import GrantResponse, GrantListResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/grants", tags=["Grants"])


@router.get("", response_model=GrantListResponse)
def list_grants(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    source_type: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all grants with optional filtering and pagination"""
    query = db.query(Grant)

    # Apply filters
    if status:
        query = query.filter(Grant.status == status)
    if source_type:
        query = query.filter(Grant.source_type == source_type)
    if min_amount:
        query = query.filter(Grant.amount_max >= min_amount)
    if max_amount:
        query = query.filter(Grant.amount_min <= max_amount)

    # Count total
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    grants = query.order_by(Grant.deadline.asc()).offset(offset).limit(page_size).all()

    # Convert JSON strings to lists for response
    grants_response = []
    for grant in grants:
        grant_dict = {
            "id": grant.id,
            "source_name": grant.source_name,
            "source_url": grant.source_url,
            "source_type": grant.source_type,
            "title": grant.title,
            "description": grant.description,
            "amount_min": grant.amount_min,
            "amount_max": grant.amount_max,
            "deadline": grant.deadline,
            "application_opens": grant.application_opens,
            "eligibility_criteria": json.loads(grant.eligibility_criteria) if grant.eligibility_criteria else None,
            "required_documents": json.loads(grant.required_documents) if grant.required_documents else None,
            "application_url": grant.application_url,
            "contact_email": grant.contact_email,
            "contact_phone": grant.contact_phone,
            "geographic_restriction": grant.geographic_restriction,
            "target_populations": json.loads(grant.target_populations) if grant.target_populations else None,
            "funding_priorities": json.loads(grant.funding_priorities) if grant.funding_priorities else None,
            "status": grant.status,
            "discovered_at": grant.discovered_at,
            "last_updated": grant.last_updated
        }
        grants_response.append(grant_dict)

    return {
        "grants": grants_response,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{grant_id}", response_model=GrantResponse)
def get_grant(
    grant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific grant by ID"""
    grant = db.query(Grant).filter(Grant.id == grant_id).first()

    if not grant:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grant not found"
        )

    # Convert JSON strings to lists
    grant_dict = {
        "id": grant.id,
        "source_name": grant.source_name,
        "source_url": grant.source_url,
        "source_type": grant.source_type,
        "title": grant.title,
        "description": grant.description,
        "amount_min": grant.amount_min,
        "amount_max": grant.amount_max,
        "deadline": grant.deadline,
        "application_opens": grant.application_opens,
        "eligibility_criteria": json.loads(grant.eligibility_criteria) if grant.eligibility_criteria else None,
        "required_documents": json.loads(grant.required_documents) if grant.required_documents else None,
        "application_url": grant.application_url,
        "contact_email": grant.contact_email,
        "contact_phone": grant.contact_phone,
        "geographic_restriction": grant.geographic_restriction,
        "target_populations": json.loads(grant.target_populations) if grant.target_populations else None,
        "funding_priorities": json.loads(grant.funding_priorities) if grant.funding_priorities else None,
        "status": grant.status,
        "discovered_at": grant.discovered_at,
        "last_updated": grant.last_updated
    }

    return grant_dict
