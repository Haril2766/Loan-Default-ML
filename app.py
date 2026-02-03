from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np
import pandas as pd
import os

# -----------------------------
# App setup
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Load ML model safely
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "loan_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print("❌ Model load failed:", e)

# -----------------------------
# Constants
# -----------------------------
EDUCATION_OPTIONS = ["High School", "Bachelor's", "Master's", "PhD"]
EMPLOYMENT_OPTIONS = ["Full-time", "Part-time", "Self-employed", "Unemployed"]

SOCIAL_LINKS = {
    "linkedin": "https://www.linkedin.com/in/bhavy-soni-6123a32b0/",
    "github": "https://github.com/Bhavy123321"
}

REVIEWS = [
    {
        "name": "Aarav",
        "rating": 5,
        "message": "Clean UI and super fast prediction. Loved it!",
        "tag": "Student"
    },
    {
        "name": "Neha",
        "rating": 4,
        "message": "Very smooth experience. Looks professional.",
        "tag": "Developer"
    }
]

# -----------------------------
# Helpers
# -----------------------------
def to_float(value, field_name):
    try:
        v = float(value)
        if np.isnan(v) or np.isinf(v):
            raise ValueError
        return v
    except Exception:
        raise ValueError(f"Invalid value for {field_name}")

@app.context_processor
def inject_globals():
    return dict(social=SOCIAL_LINKS)

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template(
        "index.html",
        education_options=EDUCATION_OPTIONS,
        employment_options=EMPLOYMENT_OPTIONS
    )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/reviews", methods=["GET"])
def reviews():
    return render_template("reviews.html", reviews=list(reversed(REVIEWS)))

@app.route("/reviews", methods=["POST"])
def add_review():
    name = (request.form.get("name") or "Anonymous")[:40]
    tag = (request.form.get("tag") or "User")[:30]
    message = (request.form.get("message") or "Great project!")[:300]

    try:
        rating = int(request.form.get("rating", 5))
    except Exception:
        rating = 5

    rating = max(1, min(5, rating))

    REVIEWS.append({
        "name": name,
        "rating": rating,
        "message": message,
        "tag": tag
    })

    return redirect(url_for("reviews"))

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return render_template(
            "index.html",
            education_options=EDUCATION_OPTIONS,
            employment_options=EMPLOYMENT_OPTIONS,
            error="Model not loaded on server."
        )

    try:
        age = to_float(request.form.get("Age"), "Age")
        income = to_float(request.form.get("Income"), "Income")
        loan_amount = to_float(request.form.get("LoanAmount"), "Loan Amount")
        credit_score = to_float(request.form.get("CreditScore"), "Credit Score")
        dti = to_float(request.form.get("DTIRatio"), "DTI Ratio")

        education = request.form.get("Education")
        employment = request.form.get("EmploymentType")

        if education not in EDUCATION_OPTIONS:
            raise ValueError("Invalid education selection")
        if employment not in EMPLOYMENT_OPTIONS:
            raise ValueError("Invalid employment selection")

        X = pd.DataFrame([{
            "Age": age,
            "Income": income,
            "LoanAmount": loan_amount,
            "CreditScore": credit_score,
            "DTIRatio": dti,
            "Education": education,
            "EmploymentType": employment
        }])

        pred = int(model.predict(X)[0])

        try:
            proba = float(model.predict_proba(X)[0][1])
        except Exception:
            proba = None

        status = "Approved ✅" if pred == 0 else "Rejected ❌"

        confidence = None
        if proba is not None:
            confidence = round((1 - proba) * 100, 2) if pred == 0 else round(proba * 100, 2)

        hints = []
        if credit_score < 650:
            hints.append("Low Credit Score")
        if dti > 0.45:
            hints.append("High DTI Ratio")
        if income > 0 and loan_amount > income * 0.6:
            hints.append("Loan amount high compared to income")

        return render_template(
            "result.html",
            status=status,
            confidence=confidence,
            proba=None if proba is None else round(proba * 100, 2),
            age=age,
            income=income,
            loan_amount=loan_amount,
            credit_score=credit_score,
            dti=dti,
            education=education,
            employment=employment,
            hints=hints
        )

    except Exception as e:
        return render_template(
            "index.html",
            education_options=EDUCATION_OPTIONS,
            employment_options=EMPLOYMENT_OPTIONS,
            error=str(e),
            form=request.form
        )

# -----------------------------
# Health check (IMPORTANT)
# -----------------------------
@app.route("/health")
def health():
    return "OK", 200

# -----------------------------
# Entry point (local only)
# -----------------------------
if __name__ == "__main__":
    app.run()
