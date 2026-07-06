import serial
import pandas as pd
from datetime import datetime
import os

PORT = "COM7"          # Change if your ESP32 is on another COM port
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)

os.makedirs("data", exist_ok=True)

csv_file = "data/live_machine_data.csv"

# Create CSV if it doesn't exist
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=[
        "Timestamp",
        "Voltage",
        "Current",
        "Power",
        "PowerFactor",
        "Frequency"
    ])
    df.to_csv(csv_file, index=False)

print("Listening to ESP32...")

while True:
    try:
        line = ser.readline().decode().strip()

        if not line:
            continue

        values = line.split(",")

        if len(values) != 5:
            continue

        voltage = float(values[0])
        current = float(values[1])
        power = float(values[2])
        pf = float(values[3])
        frequency = float(values[4])

        timestamp = datetime.now()

        print(
            timestamp,
            voltage,
            current,
            power,
            pf,
            frequency
        )

        row = pd.DataFrame([{
            "Timestamp": timestamp,
            "Voltage": voltage,
            "Current": current,
            "Power": power,
            "PowerFactor": pf,
            "Frequency": frequency
        }])

        row.to_csv(csv_file, mode="a", header=False, index=False)

    except KeyboardInterrupt:
        ser.close()
        print("Stopped")
        break

    except Exception as e:
        print(e)