
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle

# Create flask app
app = Flask(__name__)

# Load the trained model
model = pickle.load(open("model.pkl", "rb"))

# Load feature names used during training
feature_names = ['MonthlyIncome', 'StockOptionLevel', 'YearsWithCurrManager',
       'OverTime_Yes', 'JobIncomeInteraction']


@app.route("/")
def Home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def predict():
    # Retrieve form values as a list of floats
    float_features = [float(x) for x in request.form.values()]
    
    # Ensure the input matches the expected feature names
    input_data = pd.DataFrame([float_features], columns=feature_names)
    
    # Make prediction using the loaded model
    prediction = model.predict(input_data)
    
    # Format the prediction result
    if prediction[0] == 0:
        prediction_text = f"Result : {prediction[0]} (NO)"
    else:
        prediction_text = f"Result : {prediction[0]} (YES)"
    
    # Render the result on the home page
    return render_template("home.html", prediction_text=prediction_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
    