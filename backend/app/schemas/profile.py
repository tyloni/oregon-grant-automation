from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProfileBase(BaseModel):
    organization_name: str
    organization_type: Optional[str] = None
    tax_id: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: str = "OR"
    zip_code: Optional[str] = None
    county: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    mission_statement: Optional[str] = None
    established_year: Optional[int] = None
    current_enrollment: Optional[int] = None
    max_capacity: Optional[int] = None
    age_range_served: Optional[str] = None
    operating_budget: Optional[float] = None
    staff_count: Optional[int] = None
    licensed: bool = False
    license_number: Optional[str] = None
    accreditations: Optional[List[str]] = None
    populations_served: Optional[List[str]] = None
    rural_or_urban: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    organization_name: Optional[str] = None


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    updated_at: datetime

    class Config:
        from_attributes = True
