from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Grant(Base):
    __tablename__ = "grants"

    id = Column(Integer, primary_key=True, index=True)

    # Source Information
    source_name = Column(String, nullable=False, index=True)
    source_url = Column(String)
    source_type = Column(String)  # 'state', 'federal', 'foundation', 'private'

    # Grant Details
    title = Column(String, nullable=False, index=True)
    description = Column(Text)

    # Funding
    amount_min = Column(Float)
    amount_max = Column(Float)

    # Timeline
    deadline = Column(DateTime(timezone=True), index=True)
    application_opens = Column(DateTime(timezone=True))

    # Requirements
    eligibility_criteria = Column(Text)  # JSON
    required_documents = Column(Text)  # JSON array

    # Application Info
    application_url = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)

    # Targeting
    geographic_restriction = Column(String)  # 'statewide', 'rural', specific counties
    target_populations = Column(Text)  # JSON array
    funding_priorities = Column(Text)  # JSON array

    # Metadata
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status = Column(String, default="active")  # 'active', 'closed', 'archived'

    # Relationships
    matches = relationship("GrantMatch", back_populates="grant")
    applications = relationship("Application", back_populates="grant")


class GrantMatch(Base):
    __tablename__ = "grant_matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    grant_id = Column(Integer, ForeignKey("grants.id"), nullable=False)

    # Scores
    eligibility_score = Column(Float)  # 0-100
    success_likelihood_score = Column(Float)  # 0-100
    effort_score = Column(Float)  # 0-100 (lower is better)
    overall_score = Column(Float)  # weighted composite

    # Explanation
    match_reasons = Column(Text)  # JSON array of why it matches

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="grant_matches")
    grant = relationship("Grant", back_populates="matches")


class ScraperJob(Base):
    __tablename__ = "scraper_jobs"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, nullable=False)
    source_url = Column(String, nullable=False)

    last_run = Column(DateTime(timezone=True))
    next_run = Column(DateTime(timezone=True))

    status = Column(String)  # 'success', 'failed', 'running'
    grants_found = Column(Integer, default=0)
    error_message = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
