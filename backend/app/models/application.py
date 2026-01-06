from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    grant_id = Column(Integer, ForeignKey("grants.id"), nullable=False)

    # Status
    status = Column(String, default="draft")  # 'draft', 'in_review', 'submitted', 'won', 'lost'

    # Content - store as JSON text
    sections = Column(Text)  # JSON with all application sections

    # Output
    output_format = Column(String)  # 'pdf', 'docx'
    file_path = Column(String)  # path to generated document

    # Submission & Outcome
    submitted_at = Column(DateTime(timezone=True))
    outcome = Column(String)  # 'pending', 'awarded', 'rejected', NULL
    amount_awarded = Column(Float)
    notes = Column(Text)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="applications")
    grant = relationship("Grant", back_populates="applications")
    attachments = relationship("ApplicationAttachment", back_populates="application", cascade="all, delete-orphan")


class ApplicationAttachment(Base):
    __tablename__ = "application_attachments"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)

    file_name = Column(String, nullable=False)
    file_type = Column(String)  # 'budget', 'certificate', 'letter', 'other'
    file_path = Column(String, nullable=False)

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    application = relationship("Application", back_populates="attachments")


class SuccessTemplate(Base):
    __tablename__ = "success_templates"

    id = Column(Integer, primary_key=True, index=True)
    grant_source_name = Column(String)  # to match similar grants
    application_id = Column(Integer, ForeignKey("applications.id"))

    # Template data
    winning_strategies = Column(Text)  # JSON: key elements that worked
    template_sections = Column(Text)  # JSON: reusable content templates

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    application = relationship("Application")
