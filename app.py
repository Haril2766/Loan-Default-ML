from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except:
    model = None

@app.route("/")
@app.route("/")
def home():
    education_options = ["High School", "Bachelor's", "Master's", "PhD"]
    employment_options = ["Unemployed", "Part-time", "Full-time", "Self-employed"]

    return render_template(
        "index.html",
        education_options=education_options,
        employment_options=employment_options
    )
@app.route("/predict", methods=["POST"])
def predict():

    if model is None:
        return "Model not loaded"

    try:
        age = float(request.form.get("Age"))
        income = float(request.form.get("Income"))
        loan_amount = float(request.form.get("LoanAmount"))
        loan_term = float(request.form.get("LoanTerm"))
        credit_score = float(request.form.get("CreditScore"))
        dti = float(request.form.get("DTIRatio"))
        education = request.form.get("Education")
        employment = request.form.get("EmploymentType")

        # 🔥 Missing training features → fill default
        marital = 0
        purpose = 0

        # ---- Label Encoding ----
        edu_map = {"High School":0, "Bachelor's":1, "Master's":2, "PhD":3}
        emp_map = {"Unemployed":0, "Part-time":1, "Full-time":2, "Self-employed":3}

        education = edu_map.get(education,0)
        employment = emp_map.get(employment,0)

        # ---- Create base ----
        features = [
            age, income, loan_amount, loan_term,
            credit_score, dti,
            education, employment,
            marital, purpose
        ]

        # ---- Ensure 16 features ----
        while len(features) < 16:
            features.append(0)

        X = pd.DataFrame([features])

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
            education=request.form.get("Education"),
            employment=request.form.get("EmploymentType")
        )

    except Exception as e:
        return str(e)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

