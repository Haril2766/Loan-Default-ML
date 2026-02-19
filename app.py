from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model + scaler + encoder
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
encoder = joblib.load(os.path.join(BASE_DIR, "encoder.pkl"))

print("✅ Model + Scaler + Encoder Loaded")

EDUCATION_OPTIONS = ["High School", "Bachelor's", "Master's", "PhD"]
EMPLOYMENT_OPTIONS = ["Full-time", "Part-time", "Self-employed", "Unemployed"]

def to_float(value):
    return float(value)

@app.route("/")
def home():
    return render_template(
        "index.html",
        education_options=EDUCATION_OPTIONS,
        employment_options=EMPLOYMENT_OPTIONS
    )

@app.route("/predict", methods=["POST"])
def predict():

    try:
        age = to_float(request.form.get("Age"))
        income = to_float(request.form.get("Income"))
        loan_amount = to_float(request.form.get("LoanAmount"))
        loan_term = to_float(request.form.get("LoanTerm"))
        credit_score = to_float(request.form.get("CreditScore"))
        dti = to_float(request.form.get("DTIRatio"))

        education = request.form.get("Education")
        employment = request.form.get("EmploymentType")

        # Raw input dataframe
        X = pd.DataFrame([{
            "Age": age,
            "Income": income,
            "LoanAmount": loan_amount,
            "LoanTerm": loan_term,
            "CreditScore": credit_score,
            "DTIRatio": dti,
            "Education": education,
            "EmploymentType": employment
        }])

        # 🚨 APPLY SAME TRAINING PIPELINE
        encoded = encoder.transform(X)
        scaled = scaler.transform(encoded)

        pred = int(model.predict(scaled)[0])

        try:
            proba = float(model.predict_proba(scaled)[0][1])
        except:
            proba = None

        status = "Approved ✅" if pred == 0 else "Rejected ❌"

        confidence = None
        if proba is not None:
            confidence = round((1 - proba) * 100, 2) if pred == 0 else round(proba * 100, 2)

        return render_template(
            "result.html",
            status=status,
            confidence=confidence,
            age=age,
            income=income,
            loan_amount=loan_amount,
            loan_term=loan_term,
            credit_score=credit_score,
            dti=dti,
            education=education,
            employment=employment
        )

    except Exception as e:
        print("Prediction Error:", e)
        return redirect("/")

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run()
