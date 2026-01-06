from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.grant import Grant
from app.models.application import Application
from app.schemas.application import (
    ApplicationGenerateRequest,
    ApplicationGenerateResponse,
    ApplicationRefineRequest,
    ApplicationResponse,
    ApplicationListResponse
)
from app.services.llm_service import generate_grant_application, refine_section, generate_personalization_suggestion
from app.services.auth_service import get_current_user
from typing import Dict, Any
from pydantic import BaseModel
import json
from datetime import datetime

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/generate", response_model=ApplicationGenerateResponse, status_code=status.HTTP_201_CREATED)
def generate_application(
    request: ApplicationGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a grant application using AI based on grant details and organization data
    """
    # Fetch the grant
    grant = db.query(Grant).filter(Grant.id == request.grant_id).first()
    if not grant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grant with id {request.grant_id} not found"
        )

    # Prepare grant data for LLM
    # Parse JSON fields
    eligibility_criteria = json.loads(grant.eligibility_criteria) if grant.eligibility_criteria else []
    funding_priorities = json.loads(grant.funding_priorities) if grant.funding_priorities else []
    required_documents = json.loads(grant.required_documents) if grant.required_documents else []

    grant_data = {
        "title": grant.title,
        "source_name": grant.source_name,
        "source_type": grant.source_type,
        "description": grant.description,
        "amount_min": grant.amount_min,
        "amount_max": grant.amount_max,
        "deadline": grant.deadline.isoformat() if grant.deadline else None,
        "eligibility_criteria": eligibility_criteria,
        "funding_priorities": funding_priorities,
        "required_documents": required_documents,
        "geographic_restriction": grant.geographic_restriction
    }

    # Prepare org data for LLM
    org_data = {
        "organization_name": request.org_data.organization_name,
        "organization_type": request.org_data.organization_type,
        "city": request.org_data.city,
        "mission_statement": request.org_data.mission_statement,
        "current_enrollment": request.org_data.current_enrollment,
        "operating_budget": request.org_data.operating_budget,
        "staff_count": request.org_data.staff_count
    }

    # Generate the application using template-based system
    try:
        print(f"Generating application for grant: {grant_data.get('title')}")
        print(f"Organization: {org_data.get('organization_name')}")
        sections = generate_grant_application(grant_data, org_data)
        print(f"Generated sections: {list(sections.keys())}")
    except Exception as e:
        print(f"Error generating application: {e}")
        import traceback
        traceback.print_exc()
        error_msg = str(e)
        # Check for quota errors
        if "429" in error_msg or "quota" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Gemini API quota exceeded. The free tier has daily limits. Please try again later or upgrade your Gemini API plan at https://ai.google.dev/pricing"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate application: {str(e)}"
        )

    # Check if there's an error in the response
    if "error" in sections:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI generation error: {sections.get('error')}"
        )

    # Create application record in database
    application = Application(
        user_id=current_user.id,
        grant_id=grant.id,
        status="draft",
        sections=json.dumps(sections),  # Store as JSON string
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return ApplicationGenerateResponse(
        id=application.id,
        grant_id=grant.id,
        grant_title=grant.title,
        status=application.status,
        sections=json.loads(application.sections) if application.sections else {},
        created_at=application.created_at
    )


@router.get("", response_model=ApplicationListResponse)
def list_applications(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all applications for the current user
    """
    offset = (page - 1) * page_size

    # Get applications with grant info
    query = db.query(Application).filter(Application.user_id == current_user.id)
    total = query.count()
    applications = query.order_by(Application.created_at.desc()).offset(offset).limit(page_size).all()

    # Format response
    application_list = []
    for app in applications:
        grant = db.query(Grant).filter(Grant.id == app.grant_id).first()
        application_list.append(
            ApplicationResponse(
                id=app.id,
                grant_id=app.grant_id,
                grant_title=grant.title if grant else "Unknown Grant",
                status=app.status,
                sections=json.loads(app.sections) if app.sections else {},
                created_at=app.created_at,
                updated_at=app.updated_at
            )
        )

    return ApplicationListResponse(
        applications=application_list,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific application by ID
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with id {application_id} not found"
        )

    grant = db.query(Grant).filter(Grant.id == application.grant_id).first()

    return ApplicationResponse(
        id=application.id,
        grant_id=application.grant_id,
        grant_title=grant.title if grant else "Unknown Grant",
        status=application.status,
        sections=json.loads(application.sections) if application.sections else {},
        created_at=application.created_at,
        updated_at=application.updated_at
    )


@router.post("/{application_id}/refine", response_model=ApplicationResponse)
def refine_application_section(
    application_id: int,
    request: ApplicationRefineRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Refine a specific section of an application based on user feedback
    """
    # Get the application
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with id {application_id} not found"
        )

    # Check if the section exists
    sections = json.loads(application.sections) if application.sections else {}
    if request.section_name not in sections:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Section '{request.section_name}' not found in application"
        )

    # Refine the section using LLM
    try:
        original_text = sections[request.section_name]
        refined_text = refine_section(original_text, request.feedback)

        # Update the section
        sections[request.section_name] = refined_text
        application.sections = json.dumps(sections)
        application.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(application)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refine section: {str(e)}"
        )

    grant = db.query(Grant).filter(Grant.id == application.grant_id).first()

    return ApplicationResponse(
        id=application.id,
        grant_id=application.grant_id,
        grant_title=grant.title if grant else "Unknown Grant",
        status=application.status,
        sections=json.loads(application.sections) if application.sections else {},
        created_at=application.created_at,
        updated_at=application.updated_at
    )


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    sections: Dict[str, str],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually update application sections (for direct editing)
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with id {application_id} not found"
        )

    # Update sections
    application.sections = json.dumps(sections)
    application.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(application)

    grant = db.query(Grant).filter(Grant.id == application.grant_id).first()

    return ApplicationResponse(
        id=application.id,
        grant_id=application.grant_id,
        grant_title=grant.title if grant else "Unknown Grant",
        status=application.status,
        sections=json.loads(application.sections) if application.sections else {},
        created_at=application.created_at,
        updated_at=application.updated_at
    )


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an application
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with id {application_id} not found"
        )

    db.delete(application)
    db.commit()

    return None


class PersonalizationSuggestionRequest(BaseModel):
    field_name: str
    organization_name: str = ""
    organization_type: str = "Child Care Center"
    city: str = ""
    mission_statement: str = ""
    current_enrollment: int = 0
    operating_budget: float = 0
    staff_count: int = 0


class PersonalizationSuggestionResponse(BaseModel):
    field_name: str
    suggestion: str


@router.post("/personalization-suggestion", response_model=PersonalizationSuggestionResponse)
def get_personalization_suggestion(
    request: PersonalizationSuggestionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate an AI suggestion for a personalization field based on basic organization data
    """
    org_data = {
        "organization_name": request.organization_name,
        "organization_type": request.organization_type,
        "city": request.city,
        "mission_statement": request.mission_statement,
        "current_enrollment": request.current_enrollment,
        "operating_budget": request.operating_budget,
        "staff_count": request.staff_count
    }

    try:
        suggestion = generate_personalization_suggestion(request.field_name, org_data)
        return PersonalizationSuggestionResponse(
            field_name=request.field_name,
            suggestion=suggestion
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate suggestion: {str(e)}"
        )
