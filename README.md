# Survey Backend API

Backend API for collecting thesis survey data on trust factors in civic AI. Part of Bachelor's thesis in Data Science & Business Analytics.

## Project Overview

**Thesis Title:** Factors of Trust in Civic AI: A Quantitative Analysis of User Willingness to Share Sensitive Data for Open-Source Model Training in a Democratic Context

**Student:** Sabine Wildemann (ID: 190297)  
**Supervisor:** Prof. Daniel Ambach  
**Institution:** Digital Business University of Applied Sciences

### Research Design
- 2x2 factorial experiment (N=200 target)
- Tests effects of **Transparency** and **User Control** on data sharing willingness
- 4 experimental groups with random assignment
- Swiss FADP-compliant data collection

## Architecture
```
Frontend (Lovable)
    ↓
Survey: ailights.org/survey
    ↓
Backend API (This Project)
    ↓
PostgreSQL Database (Infomaniak Jelastic)
```

## Tech Stack

- **Framework:** FastAPI (Python 3.13)
- **Database:** PostgreSQL 16.10
- **ORM:** SQLAlchemy
- **Hosting:** Infomaniak Jelastic Cloud (Geneva, Switzerland)
- **Deployment:** Git-based deployment from GitHub

## Project Structure
```
survey-backend/
├── main.py              # FastAPI application & endpoints
├── models.py            # SQLAlchemy database models
├── database.py          # Database connection & session management
├── wsgi.py              # WSGI entry point for deployment
├── requirements.txt     # Python dependencies
├── .env                 # Database credentials (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Database Schema

### Normalized Design (Optimized for Statistical Analysis)

**Main Tables:**
1. **survey_responses** - One row per participant
   - Screener questions (Q1-Q3)
   - Experimental group assignment
   - Dependent variable (Q4: willingness)
   - Governance preferences (Q7-Q11)
   - Demographics (Q12-Q16)

2. **concern_ratings** - Q5 items (5 ratings per response)
   - Privacy, Misuse, Commercial, Trust, Security

3. **feature_importance** - Q6 items (6 ratings per response)
   - Anonymization, Swiss-only, Delete, Impact, Civic use, Time limit

## API Endpoints

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-16T20:00:00"
}
```

### `POST /api/submit`
Submit survey response

**Request Body:** See `SurveySubmission` model in `main.py`

**Response:**
```json
{
  "status": "success",
  "message": "Survey response recorded",
  "response_id": 123
}
```

### `GET /api/stats`
Get response statistics (for monitoring)

**Response:**
```json
{
  "total_responses": 42,
  "timestamp": "2025-11-16T20:00:00"
}
```

## Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL database
- Git

### Local Development

1. **Clone repository:**
```bash
git clone https://github.com/pluzgi/survey-backend.git
cd survey-backend
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run locally (without database connection):**

**Note:** Local execution requires commenting out database creation in `main.py` line 16:
```python
# Base.metadata.create_all(bind=engine)
```

Then start server:
```bash
uvicorn main:app --reload
```

Access API docs at: `http://127.0.0.1:8000/docs`

## Deployment

### Infomaniak Jelastic Cloud

**Current Status:** Code deployed, dependencies installation in progress

**Deployment URL:** `https://env-0590835.jcloud-ver-jpe.ik-server.com`

**Database Connection:**
- Host: `10.101.15.44:5432` (internal network)
- Database: `postgres`
- User: `webadmin`

### Git-Based Deployment

Code is deployed automatically from GitHub:
```
Repository: https://github.com/pluzgi/survey-backend.git
Branch: main
```

To deploy updates:
1. Commit and push changes to GitHub
2. In Jelastic dashboard: Deployments → ROOT → Update from Git

## Current Status

### ✅ Completed
- [x] Project structure created
- [x] Database models defined (normalized schema)
- [x] FastAPI endpoints implemented
- [x] Pydantic validation models
- [x] CORS configuration for Lovable frontend
- [x] Git repository initialized
- [x] Code pushed to GitHub
- [x] Infomaniak Jelastic Cloud environment created
- [x] PostgreSQL database provisioned
- [x] Code deployed to Jelastic
- [x] WSGI entry point created

### 🚧 In Progress
- [ ] Python dependencies installation on server
- [ ] FastAPI service startup configuration
- [ ] Database table creation in production
- [ ] API endpoint testing in production

### 📋 Next Steps

#### 1. Fix Deployment Issues (Priority: HIGH)

**Problem:** Dependencies not installing automatically on Jelastic

**Solutions to try:**
1. **Add Jelastic deployment hooks:**
   - Create `/.jelastic/scripts/deploy.sh`
   - Add pip install command

2. **Manual SSH installation:**
   - Connect via SSH: `ssh 189663-10200@gate.jpe.infomaniak.com -p 3022`
   - Navigate to: `cd /var/www/webroot/ROOT`
   - Install: `pip install -r requirements.txt --break-system-packages`

3. **Alternative: Pre-install in Docker/container**
   - Contact Jelastic support for Python environment configuration

4. **Check Jelastic Python documentation:**
   - Review: https://docs.jelastic.com/python-center

#### 2. Verify Database Connection

Once app starts:
```bash
# Test database tables were created
# Access PostgreSQL via Jelastic dashboard
# Verify tables: survey_responses, concern_ratings, feature_importance
```

#### 3. Test API Endpoints
```bash
# Health check
curl https://env-0590835.jcloud-ver-jpe.ik-server.com/health

# API documentation
# Visit: https://env-0590835.jcloud-ver-jpe.ik-server.com/docs
```

#### 4. Connect Lovable Frontend

In Lovable project, update API endpoint:
```javascript
const API_URL = 'https://env-0590835.jcloud-ver-jpe.ik-server.com';
```

#### 5. Test End-to-End Flow

1. Complete survey on ailights.org/survey
2. Verify data appears in PostgreSQL
3. Check `/api/stats` endpoint for count

#### 6. Data Export for Analysis

Once data collected, export for Python analysis:
```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)

# Export responses
df_responses = pd.read_sql("SELECT * FROM survey_responses", engine)

# Export concerns (for factor analysis)
df_concerns = pd.read_sql("SELECT * FROM concern_ratings", engine)

# Export features
df_features = pd.read_sql("SELECT * FROM feature_importance", engine)

# Merge for analysis
df_full = df_responses.merge(df_concerns, on='response_id')

# Export to CSV
df_full.to_csv('survey_data.csv', index=False)
```

#### 7. Statistical Analysis (Post-Collection)

**Tools:** Python (pandas, statsmodels, scikit-learn)

**Analysis steps:**
1. Descriptive statistics
2. Factor analysis on Q5 concerns
3. Ordinal logistic regression:
   - DV: Willingness (Q4)
   - IV: Transparency, Control, Interaction
   - Covariates: Demographics, tech affinity, concerns

## Troubleshooting

### Database Connection Errors Locally

**Error:** `connection to server at "10.101.15.44", port 5432 failed`

**Solution:** Database only accessible from Jelastic network. Comment out line 16 in `main.py` for local testing.

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Activate virtual environment and install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### CORS Errors from Lovable

**Error:** `Access to fetch at '...' from origin 'https://ailights.org' has been blocked by CORS`

**Solution:** Verify `allow_origins` in `main.py` includes your domain.

## Data Privacy & Compliance

- ✅ Data stored in Switzerland (Infomaniak Geneva DC4)
- ✅ Swiss FADP compliant infrastructure
- ✅ Anonymous survey design (no PII collected)
- ✅ Sensitive data classification acknowledged (political views)
- ✅ PostgreSQL access restricted to internal network

## Dependencies

See `requirements.txt`:
```
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
pydantic
python-dotenv
pydantic-settings
```

## Git Workflow
```bash
# Make changes
git add .
git commit -m "Description of changes"

# Push to GitHub (triggers potential auto-deploy)
git push

# In Jelastic: manually update from Git if needed
```

## Support & Documentation

- **FastAPI Docs:** https://fastapi.tiangolo.com
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org
- **Jelastic Python Docs:** https://docs.jelastic.com/python-center
- **Infomaniak Support:** https://www.infomaniak.com/en/support

## License

Academic research project - MIT License

## Contact

Sabine Wildemann  
Digital Business University of Applied Sciences  
Student ID: 190297

---

**Last Updated:** November 16, 2025  
**Status:** Deployment in progress