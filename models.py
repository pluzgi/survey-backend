#models.py

# Import SQLAlchemy components for defining database tables
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# Main responses table - one row per survey submission
class SurveyResponse(Base):
    __tablename__ = "survey_responses"
    
    # Primary key - unique ID for each response
    id = Column(Integer, primary_key=True, index=True)
    
    # Timestamp when survey was submitted
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Section I: Screener & Context
    q1_eligible = Column(Boolean)  # Swiss citizen eligible to vote
    q2_participation = Column(Integer)  # 1-5 scale: ballot participation frequency
    q3_tech_comfort = Column(Integer)  # 1-5 scale: technology comfort level
    
    # Section II: Experimental condition (which vignette group)
    experimental_group = Column(String)  # "group1", "group2", "group3", "group4"
    
    # Section III: Dependent variable
    q4_willingness = Column(Integer)  # 1-5 scale: willingness to share data
    
    # Section IV: Governance preferences
    q7_data_usage = Column(String)  # Who can use data (single choice)
    q8_question_usage = Column(String)  # How questions can be used (single choice)
    q9_retention_time = Column(String)  # How long to keep data (single choice)
    q10_server_location = Column(String)  # Where data should be stored (single choice)
    q11_open_response = Column(Text, nullable=True)  # Optional: main reason for decision
    
    # Section V: Demographics
    q12_age = Column(String)  # Age group
    q13_gender = Column(String)  # Gender identity
    q14_canton = Column(String)  # Swiss canton
    q15_language = Column(String)  # Primary language
    q16_education = Column(String)  # Education level
    
    # Relationships to related tables (one response has many concern ratings, etc.)
    concerns = relationship("ConcernRating", back_populates="response", cascade="all, delete-orphan")
    features = relationship("FeatureImportance", back_populates="response", cascade="all, delete-orphan")


# Q5: Concern ratings - 5 items per response (Privacy, Misuse, Commercial, Trust, Security)
class ConcernRating(Base):
    __tablename__ = "concern_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key linking to survey response
    response_id = Column(Integer, ForeignKey("survey_responses.id"))
    
    # Which concern item (privacy, misuse, commercial, trust, security)
    concern_type = Column(String)
    
    # Rating value (1-5 scale)
    rating = Column(Integer)
    
    # Relationship back to main response
    response = relationship("SurveyResponse", back_populates="concerns")


# Q6: Feature importance ratings - 6 items per response
class FeatureImportance(Base):
    __tablename__ = "feature_importance"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key linking to survey response
    response_id = Column(Integer, ForeignKey("survey_responses.id"))
    
    # Which feature (anonymization, swiss_only, delete, impact, civic_use, time_limit)
    feature_type = Column(String)
    
    # Rating value (1-5 scale)
    rating = Column(Integer)
    
    # Relationship back to main response
    response = relationship("SurveyResponse", back_populates="features")