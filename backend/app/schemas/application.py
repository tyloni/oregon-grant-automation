from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class OrganizationData(BaseModel):
    """Quick organization data for application generation"""
    organization_name: str = Field(..., min_length=1, max_length=200)
    organization_type: str = Field(..., description="e.g., 'Preschool', 'Child Care Center', 'Family Child Care'")
    city: str = Field(..., min_length=1, max_length=100)
    mission_statement: str = Field(..., min_length=10, max_length=1000)
    current_enrollment: int = Field(..., ge=0)
    operating_budget: float = Field(..., ge=0)
    staff_count: int = Field(..., ge=0)


class ApplicationGenerateRequest(BaseModel):
    """Request to generate a grant application"""
    grant_id: int = Field(..., description="ID of the grant to apply for")
    org_data: OrganizationData


class ApplicationSection(BaseModel):
    """A single section of the application"""
    section_name: str
    content: str
    user_edited: bool = False


class ApplicationGenerateResponse(BaseModel):
    """Response after generating application"""
    id: int
    grant_id: int
    grant_title: str
    status: str
    sections: Dict[str, str]
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationRefineRequest(BaseModel):
    """Request to refine a specific section"""
    section_name: str = Field(..., description="Name of section to refine (e.g., 'executive_summary')")
    feedback: str = Field(..., min_length=10, max_length=2000, description="Feedback or instructions for refinement")


class ApplicationResponse(BaseModel):
    """Full application response"""
    id: int
    grant_id: int
    grant_title: str
    status: str
    sections: Dict[str, str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationListResponse(BaseModel):
    """List of applications"""
    applications: list[ApplicationResponse]
    total: int
    page: int
    page_size: int
