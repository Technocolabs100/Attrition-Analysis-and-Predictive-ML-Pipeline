# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR  /Employee_Attrition_Prediction
ADD . /Employee_Attrition_Prediction


# Install dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 5004

# Run the application
CMD ["python", "app.py"]