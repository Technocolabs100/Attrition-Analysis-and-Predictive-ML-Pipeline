import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

# Load your dataset
data = pd.read_csv('C:/Users/muzam/OneDrive/Desktop/Attrition-Analysis/data/raw/employee_data.csv')  # Replace with your dataset path

# Select numerical features for scaling
numerical_features = ['Age', 'MonthlyIncome', 'YearsAtCompany', 'TotalWorkingYears', 'JobLevel']  # Update as needed

# Train the scaler
scaler = StandardScaler()
scaler.fit(data[numerical_features])

# Save the scaler
with open('./scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)
