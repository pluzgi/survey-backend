# main.py

# Import FastAPI and related components
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Import our database models and session
from database import get_db, engine, Base
from models import SurveyResponse, ConcernRating, FeatureImportance

# Create all database tables if they don't exist
# Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="Survey Backend API", version="1.0.0")

# Configure CORS to allow requests from Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ailights.org", "http://localhost:3000"],  # Add your Lovable domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Pydantic models for request validation
# These define the structure of data we expect from Lovable

# Individual concern rating (Q5)
class ConcernRatingData(BaseModel):
    concern_type: str  # "privacy", "misuse", "commercial", "trust", "security"
    rating: int  # 1-5 scale

# Individual feature importance rating (Q6)
class FeatureImportanceData(BaseModel):
    feature_type: str  # "anonymization", "swiss_only", "delete", "impact", "civic_use", "time_limit"
    rating: int  # 1-5 scale

# Complete survey submission data
class SurveySubmission(BaseModel):
    # Section I: Screener & Context
    q1_eligible: bool
    q2_participation: int
    q3_tech_comfort: int
    
    # Section II: Experimental condition
    experimental_group: str  # "group1", "group2", "group3", "group4"
    
    # Section III: Dependent variable
    q4_willingness: int
    
    # Section IV: Attitudinal variables
    concerns: List[ConcernRatingData]  # 5 items for Q5
    features: List[FeatureImportanceData]  # 6 items for Q6
    
    # Section IV: Governance preferences
    q7_data_usage: str
    q8_question_usage: str
    q9_retention_time: str
    q10_server_location: str
    q11_open_response: Optional[str] = None  # Optional field
    
    # Section V: Demographics
    q12_age: str
    q13_gender: str
    q14_canton: str
    q15_language: str
    q16_education: str


# API Endpoints

# Health check endpoint - verify API is running
@app.get("/health")
def health_check():
    """Simple health check to verify API is operational"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


# Main endpoint to receive survey submissions from Lovable
@app.post("/api/submit")
def submit_survey(
    submission: SurveySubmission,
    db: Session = Depends(get_db)  # Inject database session
):
    """
    Receive survey submission from Lovable frontend and store in PostgreSQL
    Returns success message with response ID
    """
    try:
        # Create main survey response record
        response = SurveyResponse(
            q1_eligible=submission.q1_eligible,
            q2_participation=submission.q2_participation,
            q3_tech_comfort=submission.q3_tech_comfort,
            experimental_group=submission.experimental_group,
            q4_willingness=submission.q4_willingness,
            q7_data_usage=submission.q7_data_usage,
            q8_question_usage=submission.q8_question_usage,
            q9_retention_time=submission.q9_retention_time,
            q10_server_location=submission.q10_server_location,
            q11_open_response=submission.q11_open_response,
            q12_age=submission.q12_age,
            q13_gender=submission.q13_gender,
            q14_canton=submission.q14_canton,
            q15_language=submission.q15_language,
            q16_education=submission.q16_education
        )
        
        # Add to database session
        db.add(response)
        db.flush()  # Get the response ID without committing yet
        
        # Create concern rating records (Q5 - 5 items)
        for concern in submission.concerns:
            concern_record = ConcernRating(
                response_id=response.id,
                concern_type=concern.concern_type,
                rating=concern.rating
            )
            db.add(concern_record)
        
        # Create feature importance records (Q6 - 6 items)
        for feature in submission.features:
            feature_record = FeatureImportance(
                response_id=response.id,
                feature_type=feature.feature_type,
                rating=feature.rating
            )
            db.add(feature_record)
        
        # Commit all changes to database
        db.commit()
        
        # Return success response
        return {
            "status": "success",
            "message": "Survey response recorded",
            "response_id": response.id
        }
    
    except Exception as e:
        # Rollback on error
        db.rollback()
        # Return error response
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Optional: Get total response count (for monitoring)
@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Return basic statistics about collected responses"""
    total_responses = db.query(SurveyResponse).count()
    return {
        "total_responses": total_responses,
        "timestamp": datetime.utcnow()
    }
