import requests
import json

def test_health():
    response = requests.get('http://localhost:5000/health')
    print("Health Check Response:", response.json())

def test_prediction():
    # Test data with all required features
    test_data = {
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
    
    # Make prediction request
    response = requests.post(
        'http://localhost:5000/predict',
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print("\nPrediction Response:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_health()
    test_prediction() 