from flask import Flask, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

CSV_FOLDER = "data"
CSV_FILE = os.path.join(CSV_FOLDER, "live_machine_data.csv")

# Minimum current required for recording
CURRENT_THRESHOLD = 0.20

# Create the data folder if it doesn't exist
os.makedirs(CSV_FOLDER, exist_ok=True)


@app.route("/data", methods=["POST"])
def receive_data():

    data = request.get_json(force=True)

    row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Voltage": data["voltage"],
        "Current": data["current"],
        "Frequency": data["frequency"],
        "kW": data["power"],
        "kVA": 0.0,      # Temporary until real register is added
        "PowerFactor": data["pf"]
    }

    df = pd.DataFrame([row])

    # Record only when machine is running
    if row["Current"] > CURRENT_THRESHOLD:

        if os.path.exists(CSV_FILE):
            df.to_csv(CSV_FILE, mode="a", header=False, index=False)
        else:
            df.to_csv(CSV_FILE, index=False)

        print("🟢 Recording:", row)

    else:

        print("🔵 Machine Idle - Data Not Recorded")

    return {"status": "success"}, 200


if __name__ == "__main__":
    print("====================================")
    print("Flask Server Started")
    print(f"Saving data to: {CSV_FILE}")
    print("====================================")
    app.run(host="0.0.0.0", port=5000)