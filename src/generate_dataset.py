import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Number of samples
n_samples = 3000

data = []

start_time = datetime.now()

for i in range(n_samples):

    # Healthy
    if i < 1000:
        current = np.random.uniform(4, 6)
        voltage = np.random.uniform(410, 420)
        frequency = np.random.uniform(49.8, 50.2)
        pf = np.random.uniform(0.92, 0.98)
        health = "Healthy"

    # Early Wear
    elif i < 2000:
        current = np.random.uniform(6, 8)
        voltage = np.random.uniform(410, 420)
        frequency = np.random.uniform(49.5, 50.2)
        pf = np.random.uniform(0.82, 0.92)
        health = "Early Wear"

    # Faulty
    
    else:
        current = np.random.uniform(8, 12)
        voltage = np.random.uniform(405, 420)
        frequency = np.random.uniform(49.0, 50.0)
        pf = np.random.uniform(0.60, 0.82)
        health = "Faulty"

    # Derived values
    kva = (voltage * current) / 1000
    kw = kva * pf

    timestamp = start_time + timedelta(minutes=i)

    data.append([
        timestamp,
        voltage,
        current,
        frequency,
        kw,
        kva,
        pf,
        health
    ])

# Create DataFrame
df = pd.DataFrame(
    data,
    columns=[
        "Timestamp",
        "Voltage",
        "Current",
        "Frequency",
        "kW",
        "kVA",
        "PowerFactor",
        "Health"
    ]
)

# Save CSV
df.to_csv("data/machine_health_data.csv", index=False)

print("Dataset created successfully!")
print(df.head())