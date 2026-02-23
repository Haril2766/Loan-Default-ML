from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    model = None
    print("❌ Model load failed:", e)

EDUCATION_OPTIONS = ["High School", "Bachelor's", "Master's", "PhD"]
EMPLOYMENT_OPTIONS = ["Full-time", "Part-time", "Self-employed", "Unemployed"]

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template(
        "index.html",
        education_options=EDUCATION_OPTIONS,
        employment_options=EMPLOYMENT_OPTIONS
    )

# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- REVIEWS ----------------
@app.route("/reviews")
def reviews():
    return render_template("review.html")

@app.route("/feedback", methods=["POST"])
def feedback():
    return render_template("review.html")

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():

    if model is None:
        return "Model failed to load"

    try:
        # GET VALUES
        age = float(request.form.get("Age"))
        income = float(request.form.get("Income"))
        loan_amount = float(request.form.get("LoanAmount"))
        loan_term = float(request.form.get("LoanTerm"))
        credit_score = float(request.form.get("CreditScore"))
        dti = float(request.form.get("DTIRatio"))
        education_text = request.form.get("Education")
        employment_text = request.form.get("EmploymentType")

        # ENCODING (must match training)
        edu_map = {
            "High School": 0,
            "Bachelor's": 1,
            "Master's": 2,
            "PhD": 3
        }

        emp_map = {
            "Unemployed": 0,
            "Part-time": 1,
            "Full-time": 2,
            "Self-employed": 3
        }

        education = edu_map.get(education_text, 0)
        employment = emp_map.get(employment_text, 0)

        # CREATE INPUT DATAFRAME
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

        # PREDICT
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
            education=education_text,
            employment=employment_text,
            confidence=None,
            hints=None
        )

    except Exception as e:
        return f"Prediction Error: {str(e)}"

# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    return "OK", 200

# ---------------- RAILWAY PORT ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
