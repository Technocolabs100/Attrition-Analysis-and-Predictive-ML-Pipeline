# Employee Attrition Prediction API

A dockerized Flask API for predicting employee attrition.

## Quick Start

### Using Docker (Recommended)
```bash
# Clone the repository
git clone <your-repo-url>
cd employee-attrition-api

# Build and run with Docker Compose
docker-compose up --build
```

The API will be available at http://localhost:5000

### Local Development
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python notebooks/app.py
```

## API Endpoints

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Make Prediction
```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{
    "Age": 35,
    "BusinessTravel": "Travel_Rarely",
    "DailyRate": 1000,
    "Department": "Sales",
    "DistanceFromHome": 5,
    "Education": 3,
    "EducationField": "Life Sciences",
    "EnvironmentSatisfaction": 3,
    "Gender": "Male",
    "HourlyRate": 50,
    "JobInvolvement": 3,
    "JobLevel": 2,
    "JobRole": "Sales Executive",
    "JobSatisfaction": 4,
    "MaritalStatus": "Married",
    "MonthlyIncome": 5000,
    "MonthlyRate": 15000,
    "NumCompaniesWorked": 2,
    "OverTime": "No",
    "PercentSalaryHike": 15,
    "PerformanceRating": 3,
    "RelationshipSatisfaction": 3,
    "StockOptionLevel": 1,
    "TotalWorkingYears": 10,
    "TrainingTimesLastYear": 2,
    "WorkLifeBalance": 3,
    "YearsAtCompany": 5,
    "YearsInCurrentRole": 3,
    "YearsSinceLastPromotion": 1,
    "YearsWithCurrManager": 3
}'
```

## Environment Variables
Copy `.env.example` to `.env` and adjust if needed:
- `PORT`: API port (default: 5000)
- `FLASK_DEBUG`: Debug mode (default: False)

```
