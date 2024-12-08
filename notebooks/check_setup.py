import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_setup():
    # Check required files
    required_files = [
        'data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv',
        'notebooks/attrition_model.pkl',
        'notebooks/scaler.pkl',
        'notebooks/model_artifacts.pkl',
        '.env'
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        logger.error(f"Missing required files: {missing_files}")
        logger.info("Please run train_and_save_model.py first to generate model files.")
        return False

    logger.info("All required files are present!")
    return True

if __name__ == "__main__":
    check_setup() 