import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# -----------------------------
# Load Real Machine Dataset
# -----------------------------
df = pd.read_csv("data/live_machine_data.csv")

# -----------------------------
# Keep only machine RUNNING data
# -----------------------------
CURRENT_THRESHOLD = 0.20

df = df[df["Current"] > CURRENT_THRESHOLD].copy()

print(f"Training Samples : {len(df)}")

# -----------------------------
# Features
# -----------------------------
features = [
    "Voltage",
    "Current",
    "PowerFactor"
]

X = df[features]

# -----------------------------
# Normalize Features
# -----------------------------
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# -----------------------------
# Train Isolation Forest
# -----------------------------
model = IsolationForest(
    n_estimators=300,
    contamination=0.001,
    random_state=42
)
model.fit(X_scaled)

# -----------------------------
# Save everything together
# -----------------------------
joblib.dump(
    {
        "model": model,
        "scaler": scaler,
        "features": features
    },
    "models/machine_health_model.pkl"
)

print("\nModel Trained Successfully!")
print("Isolation Forest Saved.")