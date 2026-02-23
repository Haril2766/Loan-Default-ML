from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Pipeline Model loaded successfully")
except Exception as e:
    model = None
    print("❌ Model load failed:", e)

EDUCATION_OPTIONS = ["High School", "Bachelor's", "Master's", "PhD"]
EMPLOYMENT_OPTIONS = ["Full-time", "Part-time", "Self-employed", "Unemployed"]

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

@app.route("/reviews")
def reviews():
    return render_template("review.html")

@app.route("/feedback", methods=["POST"])
def feedback():
    return render_template("review.html")

@app.route("/predict", methods=["POST"])
def predict():

    if model is None:
        return "Model failed to load"

    age = float(request.form.get("Age"))
    income = float(request.form.get("Income"))
    loan_amount = float(request.form.get("LoanAmount"))
    loan_term = float(request.form.get("LoanTerm"))
    credit_score = float(request.form.get("CreditScore"))
    dti = float(request.form.get("DTIRatio"))
    education = request.form.get("Education")
    employment = request.form.get("EmploymentType")

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

    pred = int(model.predict(X)[0])
    status = "Approved ✅" if pred == 0 else "Rejected ❌"

    return render_template(
        "result.html",
        status=status,
        age=age,
        income=income,
        loan_amount=loan_amount,
        credit_score=credit_score,
        dti=dti,
        education=education,
        employment=employment,
        confidence=None,
        hints=None
    )

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
