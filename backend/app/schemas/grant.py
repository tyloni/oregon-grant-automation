from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class GrantBase(BaseModel):
    source_name: str
    source_url: Optional[str] = None
    source_type: Optional[str] = None
    title: str
    description: Optional[str] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    deadline: Optional[datetime] = None
    application_opens: Optional[datetime] = None
    eligibility_criteria: Optional[List[str]] = None
    required_documents: Optional[List[str]] = None
    application_url: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    geographic_restriction: Optional[str] = None
    target_populations: Optional[List[str]] = None
    funding_priorities: Optional[List[str]] = None


class GrantResponse(GrantBase):
    id: int
    status: str
    discovered_at: datetime
    last_updated: datetime

    class Config:
        from_attributes = True


class GrantListResponse(BaseModel):
    grants: List[GrantResponse]
    total: int
    page: int
    page_size: int
