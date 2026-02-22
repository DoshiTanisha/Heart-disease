from flask import Flask, render_template, request
import numpy as np
import joblib
import os

app = Flask(__name__)

# ================= LOAD MODEL & SCALER =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "final_model.pkl"))
X_mean = np.load(os.path.join(BASE_DIR, "X_mean.npy"))
X_std = np.load(os.path.join(BASE_DIR, "X_std.npy"))

# ================= HOME PAGE =================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # ---------- FORM INPUT ----------
            age = float(request.form["age"])
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            ap_hi = float(request.form["ap_hi"])
            ap_lo = float(request.form["ap_lo"])

            gender = int(request.form["gender"])
            cholesterol = int(request.form["cholesterol"])
            gluc = int(request.form["gluc"])
            smoke = int(request.form["smoke"])
            alco = int(request.form["alco"])
            active = int(request.form["active"])

            # ---------- FEATURE ENGINEERING ----------
            bmi = weight / ((height / 100) ** 2)

            # ---------- SCALE NUMERIC FEATURES (6 ONLY) ----------
            numeric_features = np.array([[age, height, weight, ap_hi, ap_lo, bmi]])
            numeric_scaled = (numeric_features - X_mean[:6]) / X_std[:6]

            age_s, height_s, weight_s, ap_hi_s, ap_lo_s, bmi_s = numeric_scaled[0]

            # ---------- FINAL INPUT (12 FEATURES — MATCHES MODEL) ----------
            final_input = np.array([[ 
                gender, cholesterol, gluc, smoke, alco, active,
                age_s, height_s, weight_s,
                ap_hi_s, ap_lo_s, bmi_s
            ]])

            # ---------- PREDICTION ----------
            pred = model.predict(final_input)[0]

            result = (
                "⚠️ High Risk of Heart Disease"
                if pred == 1
                else "✅ Low Risk of Heart Disease"
            )

            return render_template("result.html", prediction=result)

        except Exception as e:
            return render_template("result.html", prediction=f"Error: {e}")

    return render_template("index.html")

# ================= ROUTES =================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # ---------- FORM INPUT ----------
            age = float(request.form["age"])
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            ap_hi = float(request.form["ap_hi"])
            ap_lo = float(request.form["ap_lo"])

            gender = int(request.form["gender"])
            cholesterol = int(request.form["cholesterol"])
            gluc = int(request.form["gluc"])
            smoke = int(request.form["smoke"])
            alco = int(request.form["alco"])
            active = int(request.form["active"])

            # ---------- FEATURE ENGINEERING ----------
            bmi = weight / ((height / 100) ** 2)

            # ---------- SCALE NUMERIC FEATURES ----------
            numeric_features = np.array([[age, height, weight, ap_hi, ap_lo, bmi]])
            numeric_scaled = (numeric_features - X_mean[:6]) / X_std[:6]
            age_s, height_s, weight_s, ap_hi_s, ap_lo_s, bmi_s = numeric_scaled[0]

            # ---------- FINAL INPUT ----------
            final_input = np.array([[ 
                gender, cholesterol, gluc, smoke, alco, active,
                age_s, height_s, weight_s,
                ap_hi_s, ap_lo_s, bmi_s
            ]])

            # ---------- PREDICTION ----------
            pred = model.predict(final_input)[0]

            probability = model.predict_proba(final_input)[0][1]
            percentage = round(probability * 100, 2)
            result = "⚠️ High Risk of Heart Disease" if pred == 1 else "✅ Low Risk of Heart Disease"

            return render_template("result.html", prediction=result,risk_percentage=percentage)

        except Exception as e:
            return render_template("result.html", prediction=f"Error: {e}")

    # If GET request, just show the form
    return render_template("predict.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/accuracy")
def accuracy():
    return render_template("accuracy.html")

@app.route("/symptoms")
def symptoms():
    return render_template("symptoms.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

# ================= RUN APP =================
if __name__ == "__main__":
    print("Flask server running...")
    app.run(debug=True)
