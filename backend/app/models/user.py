from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    grant_matches = relationship("GrantMatch", back_populates="user")
    applications = relationship("Application", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Organization Info
    organization_name = Column(String, nullable=False)
    organization_type = Column(String)  # 'preschool', 'daycare', 'childcare_center'
    tax_id = Column(String)

    # Location
    street_address = Column(String)
    city = Column(String)
    state = Column(String, default="OR")
    zip_code = Column(String)
    county = Column(String)
    phone = Column(String)
    website = Column(String)

    # Mission & Background
    mission_statement = Column(Text)
    established_year = Column(Integer)

    # Capacity & Enrollment
    current_enrollment = Column(Integer)
    max_capacity = Column(Integer)
    age_range_served = Column(String)  # '0-3', '3-5', '0-5', etc.

    # Financial
    operating_budget = Column(Float)
    staff_count = Column(Integer)

    # Licensing & Accreditation
    licensed = Column(Boolean, default=False)
    license_number = Column(String)
    accreditations = Column(Text)  # JSON array

    # Target Populations
    populations_served = Column(Text)  # JSON array: low-income, disabilities, etc.
    rural_or_urban = Column(String)

    # Additional flexible fields
    additional_info = Column(Text)  # JSON for custom fields

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")
