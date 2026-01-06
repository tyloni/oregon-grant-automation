from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models.user import User, UserProfile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/profile", tags=["User Profile"])


@router.get("", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile"""
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    # Convert JSON strings to Python objects for response
    profile_dict = {
        "id": current_user.profile.id,
        "user_id": current_user.profile.user_id,
        "organization_name": current_user.profile.organization_name,
        "organization_type": current_user.profile.organization_type,
        "tax_id": current_user.profile.tax_id,
        "street_address": current_user.profile.street_address,
        "city": current_user.profile.city,
        "state": current_user.profile.state,
        "zip_code": current_user.profile.zip_code,
        "county": current_user.profile.county,
        "phone": current_user.profile.phone,
        "website": current_user.profile.website,
        "mission_statement": current_user.profile.mission_statement,
        "established_year": current_user.profile.established_year,
        "current_enrollment": current_user.profile.current_enrollment,
        "max_capacity": current_user.profile.max_capacity,
        "age_range_served": current_user.profile.age_range_served,
        "operating_budget": current_user.profile.operating_budget,
        "staff_count": current_user.profile.staff_count,
        "licensed": current_user.profile.licensed,
        "license_number": current_user.profile.license_number,
        "accreditations": json.loads(current_user.profile.accreditations) if current_user.profile.accreditations else None,
        "populations_served": json.loads(current_user.profile.populations_served) if current_user.profile.populations_served else None,
        "rural_or_urban": current_user.profile.rural_or_urban,
        "additional_info": json.loads(current_user.profile.additional_info) if current_user.profile.additional_info else None,
        "updated_at": current_user.profile.updated_at,
    }

    return profile_dict


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create user profile"""
    # Check if profile already exists
    if current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists. Use PUT to update."
        )

    # Convert lists and dicts to JSON strings
    profile_dict = profile_data.model_dump()
    if profile_dict.get("accreditations"):
        profile_dict["accreditations"] = json.dumps(profile_dict["accreditations"])
    if profile_dict.get("populations_served"):
        profile_dict["populations_served"] = json.dumps(profile_dict["populations_served"])
    if profile_dict.get("additional_info"):
        profile_dict["additional_info"] = json.dumps(profile_dict["additional_info"])

    # Create profile
    db_profile = UserProfile(user_id=current_user.id, **profile_dict)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return get_profile(current_user, db)


@router.put("", response_model=ProfileResponse)
def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Create one first."
        )

    # Update profile
    update_dict = profile_data.model_dump(exclude_unset=True)

    # Convert lists and dicts to JSON strings
    if "accreditations" in update_dict:
        update_dict["accreditations"] = json.dumps(update_dict["accreditations"])
    if "populations_served" in update_dict:
        update_dict["populations_served"] = json.dumps(update_dict["populations_served"])
    if "additional_info" in update_dict:
        update_dict["additional_info"] = json.dumps(update_dict["additional_info"])

    for key, value in update_dict.items():
        setattr(current_user.profile, key, value)

    db.commit()
    db.refresh(current_user.profile)

    return get_profile(current_user, db)
