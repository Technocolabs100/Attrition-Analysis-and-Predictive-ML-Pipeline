import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prepare_data():
    logger.info("Loading data...")
    # Load data
    df = pd.read_csv('data/raw\WA_Fn-UseC_-HR-Employee-Attrition.csv')
    
    # Drop unnecessary columns
    columns_to_drop = ['EmployeeNumber', 'EmployeeCount', 'Over18', 'StandardHours']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # Convert 'Attrition' to binary
    df['Attrition'] = (df['Attrition'] == 'Yes').astype(int)
    
    # Remove any constant columns
    constant_columns = [col for col in df.columns if df[col].nunique() == 1]
    df = df.drop(columns=constant_columns)
    
    # Convert categorical variables
    categorical_columns = df.select_dtypes(include=['object']).columns
    categorical_columns = [col for col in categorical_columns if col != 'Attrition']
    
    label_encoders = {}
    for column in categorical_columns:
        label_encoders[column] = LabelEncoder()
        df[column] = label_encoders[column].fit_transform(df[column])
    
    # Separate features and target
    X = df.drop('Attrition', axis=1)
    y = df['Attrition']
    
    return X, y, label_encoders

def train_model():
    try:
        logger.info("Starting model training...")
        # Prepare data
        X, y, label_encoders = prepare_data()
        
        print("Features:", X.columns.tolist())
        print("Data shape:", X.shape)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        model.fit(X_train_scaled, y_train)
        
        # Create models directory if it doesn't exist
        Path('notebooks').mkdir(parents=True, exist_ok=True)
        
        # Save model and scaler
        with open('notebooks/attrition_model.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        with open('notebooks/scaler.pkl', 'wb') as f:
            pickle.dump(scaler, f)
        
        # Save label encoders and feature columns
        model_artifacts = {
            'label_encoders': label_encoders,
            'feature_columns': X.columns.tolist()
        }
        with open('notebooks/model_artifacts.pkl', 'wb') as f:
            pickle.dump(model_artifacts, f)
        
        print("Model, scaler, and artifacts saved successfully!")
        
        # Test accuracy
        X_test_scaled = scaler.transform(X_test)
        accuracy = model.score(X_test_scaled, y_test)
        
        logger.info(f"Saving model to {'C:/Users\muzam\OneDrive\Desktop\Attrition-Analysis\notebooks\attrition_model.pkl'}")
        
        return accuracy
        
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        accuracy = train_model()
        print(f"Model accuracy: {accuracy:.2f}")
    except Exception as e:
        print(f"Failed to train model: {str(e)}") 