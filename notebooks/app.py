from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import pickle
import numpy as np
from pathlib import Path
from pydantic import BaseModel, ValidationError, Field, ConfigDict
from typing import Optional
import pandas as pd
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Define paths
MODEL_PATH = Path('notebooks/attrition_model.pkl')
SCALER_PATH = Path('notebooks/scaler.pkl')
ARTIFACTS_PATH = Path('notebooks/model_artifacts.pkl')

# HTML template for root endpoint
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Attrition Prediction API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; }
        .endpoint { margin-bottom: 30px; }
    </style>
</head>
<body>
    <h1>Employee Attrition Prediction API</h1>
    
    <div class="endpoint">
        <h2>Health Check</h2>
        <p>GET /health</p>
        <pre>curl http://localhost:5000/health</pre>
    </div>

    <div class="endpoint">
        <h2>Make Prediction</h2>
        <p>POST /predict</p>
        <pre>
curl -X POST http://localhost:5000/predict \\
-H "Content-Type: application/json" \\
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
}'</pre>
    </div>
</body>
</html>
"""

# Load Model, Scaler, and Artifacts
def load_models():
    try:
        logger.info("Loading model files...")
        if not all(path.exists() for path in [MODEL_PATH, SCALER_PATH, ARTIFACTS_PATH]):
            missing_files = [str(path) for path in [MODEL_PATH, SCALER_PATH, ARTIFACTS_PATH] if not path.exists()]
            logger.error(f"Missing files: {missing_files}")
            return None, None, None, None

        with open(MODEL_PATH, 'rb') as model_file:
            model = pickle.load(model_file, encoding='latin1')
        with open(SCALER_PATH, 'rb') as scaler_file:
            scaler = pickle.load(scaler_file, encoding='latin1')
        with open(ARTIFACTS_PATH, 'rb') as artifacts_file:
            artifacts = pickle.load(artifacts_file, encoding='latin1')
        
        logger.info("Model files loaded successfully")
        return model, scaler, artifacts['label_encoders'], artifacts['feature_columns']
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        return None, None, None, None

# Load all required components
model, scaler, label_encoders, feature_columns = load_models()

# Input Validation Schema
class EmployeeData(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
            }
        }
    )

    Age: int = Field(..., ge=18, le=100)
    BusinessTravel: str = Field(..., description="Business travel frequency")
    DailyRate: int = Field(..., ge=0)
    Department: str = Field(..., description="Employee department")
    DistanceFromHome: int = Field(..., ge=0)
    Education: int = Field(..., ge=1, le=5)
    EducationField: str
    EnvironmentSatisfaction: int = Field(..., ge=1, le=4)
    Gender: str
    HourlyRate: int = Field(..., ge=0)
    JobInvolvement: int = Field(..., ge=1, le=4)
    JobLevel: int = Field(..., ge=1, le=5)
    JobRole: str
    JobSatisfaction: int = Field(..., ge=1, le=4)
    MaritalStatus: str
    MonthlyIncome: float = Field(..., gt=0)
    MonthlyRate: float = Field(..., gt=0)
    NumCompaniesWorked: int = Field(..., ge=0)
    OverTime: str
    PercentSalaryHike: int = Field(..., ge=0)
    PerformanceRating: int = Field(..., ge=1, le=4)
    RelationshipSatisfaction: int = Field(..., ge=1, le=4)
    StockOptionLevel: int = Field(..., ge=0)
    TotalWorkingYears: int = Field(..., ge=0)
    TrainingTimesLastYear: int = Field(..., ge=0)
    WorkLifeBalance: int = Field(..., ge=1, le=4)
    YearsAtCompany: int = Field(..., ge=0)
    YearsInCurrentRole: int = Field(..., ge=0)
    YearsSinceLastPromotion: int = Field(..., ge=0)
    YearsWithCurrManager: int = Field(..., ge=0)

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def home():
    """Root endpoint with API documentation"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if None in (model, scaler, label_encoders, feature_columns):
        msg = "Model files not loaded. Please run train_and_save_model.py first."
        logger.warning(msg)
        return jsonify({
            "status": "unhealthy",
            "error": msg
        }), 503
    return jsonify({"status": "healthy", "model_loaded": True})

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    # Check if model is loaded
    if None in (model, scaler, label_encoders, feature_columns):
        msg = "Model not loaded. Please run train_and_save_model.py first."
        logger.warning(msg)
        return jsonify({
            "error": "Model not loaded",
            "details": msg
        }), 503

    try:
        # Get and validate input data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        logger.info("Received prediction request")
        employee = EmployeeData(**data)
        employee_dict = employee.model_dump()
        
        # Create DataFrame with feature names
        df = pd.DataFrame([employee_dict])
        
        # Ensure columns are in the correct order
        df = df.reindex(columns=feature_columns)
        
        # Encode categorical variables
        categorical_features = ['BusinessTravel', 'Department', 'EducationField', 
                              'Gender', 'JobRole', 'MaritalStatus', 'OverTime']
        
        for feature in categorical_features:
            if feature in df.columns and feature in label_encoders:
                try:
                    df[feature] = label_encoders[feature].transform(df[feature])
                except ValueError as e:
                    return jsonify({
                        "error": "Invalid category",
                        "details": f"Invalid value for {feature}. Valid values are: {label_encoders[feature].classes_.tolist()}"
                    }), 400
        
        # Scale features
        scaled_features = scaler.transform(df)
        
        # Make prediction
        prediction = model.predict(scaled_features)
        probability = model.predict_proba(scaled_features)[0][1]
        
        # Prepare response
        response = {
            "attrition_prediction": "Yes" if prediction[0] == 1 else "No",
            "attrition_probability": float(probability),
            "input_data": data
        }
        
        logger.info(f"Prediction made: {response['attrition_prediction']} with probability {response['attrition_probability']:.2f}")
        return jsonify(response)
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting server on port {port} with debug={debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
