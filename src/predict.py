import joblib
import pandas as pd

# -----------------------------
# Load Model
# -----------------------------
saved = joblib.load("models/machine_health_model.pkl")

model = saved["model"]
scaler = saved["scaler"]
features = saved["features"]

CURRENT_THRESHOLD = 0.20


def predict_health(voltage, current, frequency, kw, kva, pf):

    # -----------------------------
    # Machine Idle
    # -----------------------------
    if current <= CURRENT_THRESHOLD:

        return {
            "prediction": "Idle",
            "confidence": 100.0,
            "ahi": 100.0,
            "recommendation": "Machine is idle. Health analysis will resume automatically when operating current is detected.",
            "alert_level": "blue"
        }

    # -----------------------------
    # Running Sample
    # -----------------------------
    sample = pd.DataFrame({
        "Voltage": [voltage],
        "Current": [current],
        "PowerFactor": [pf]
    })

    sample_scaled = scaler.transform(sample)

    prediction = model.predict(sample_scaled)[0]
    score = model.decision_function(sample_scaled)[0]

    print("=" * 50)
    print(f"Current          : {current:.2f}")
    print(f"Isolation Score  : {score:.6f}")
    print(f"Prediction       : {prediction}")
    print("=" * 50)

    # -----------------------------
    # HEALTHY
    # -----------------------------
    if prediction == 1:

        confidence = max(90.0, min(99.0, 95 + score * 10))
        ahi = confidence

        return {
            "prediction": "Healthy",
            "confidence": round(confidence, 2),
            "ahi": round(ahi, 2),
            "recommendation": "Machine is operating normally. No abnormal behaviour detected.",
            "alert_level": "green"
        }

    # -----------------------------
    # WARNING
    # -----------------------------
    else:

        confidence = max(60.0, min(89.0, 80 + score * 20))
        ahi = confidence

        return {
            "prediction": "Warning",
            "confidence": round(confidence, 2),
            "ahi": round(ahi, 2),
            "recommendation": "Abnormal operating behaviour detected. Please inspect the machine if the condition persists.",
            "alert_level": "yellow"
        }